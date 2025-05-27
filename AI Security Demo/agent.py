from typing import Any, Generator, Optional

import mlflow
from databricks.sdk import WorkspaceClient
from databricks.sdk.credentials_provider import ModelServingUserCredentials
from databricks_langchain import (
    ChatDatabricks,
    VectorSearchRetrieverTool,
)
from langchain_core.language_models import LanguageModelLike
from langchain_core.runnables import RunnableConfig, RunnableLambda
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from mlflow.langchain.chat_agent_langgraph import ChatAgentState, ChatAgentToolNode
from mlflow.pyfunc import ChatAgent
from mlflow.types.agent import (
    ChatAgentChunk,
    ChatAgentMessage,
    ChatAgentResponse,
    ChatContext,
)

mlflow.langchain.autolog()

############################################
# Define your LLM endpoint and system prompt
############################################
LLM_ENDPOINT_NAME = "databricks-claude-3-7-sonnet"
llm = ChatDatabricks(endpoint=LLM_ENDPOINT_NAME)

system_prompt = ""

###############################################################################
## Define tools for your agent, enabling it to retrieve data or take actions
## beyond text generation
## To create and see usage examples of more tools, see
## https://docs.databricks.com/generative-ai/agent-framework/agent-tool.html
###############################################################################


def create_tools():
    tools = []
    # Use user authenticated client to initialize a vector search retrieval tool
    user_authenticated_client = WorkspaceClient(
        credentials_strategy=ModelServingUserCredentials()
    )
    vector_search_tools = []
    try:
        # TODO fill in fields below
        tool = VectorSearchRetrieverTool(
            index_name="dasf.ai_demo.employee_index",
            description="employee search index",
            tool_name="employee_search_tool",
            workspace_client=user_authenticated_client
        )
        vector_search_tools.append(tool)
    except Exception as e:
        print(f"Skipping Vector Search Tool: {e}")
        raise Exception("You are accessing an employee search tool that you don't have access to. Sorry for the inconvenience, but please contact your workspace admin to grant you access to the search tool.")
    tools.extend(vector_search_tools)
    return tools


#####################
## Define agent logic
#####################
def create_tool_calling_agent(
    model: LanguageModelLike,
    system_prompt: Optional[str] = None,
) -> CompiledGraph:
    tools = create_tools()  # Setup tools
    model = model.bind_tools(tools)

    # Define the function that determines which node to go to
    def should_continue(state: ChatAgentState):
        messages = state["messages"]
        last_message = messages[-1]
        # If there are function calls, continue. else, end
        if last_message.get("tool_calls"):
            return "continue"
        else:
            return "end"

    if system_prompt:
        preprocessor = RunnableLambda(
            lambda state: [{"role": "system", "content": system_prompt}]
            + state["messages"]
        )
    else:
        preprocessor = RunnableLambda(lambda state: state["messages"])
    model_runnable = preprocessor | model

    def call_model(
        state: ChatAgentState,
        config: RunnableConfig,
    ):
        response = model_runnable.invoke(state, config)

        return {"messages": [response]}

    workflow = StateGraph(ChatAgentState)

    workflow.add_node("agent", RunnableLambda(call_model))
    workflow.add_node("tools", ChatAgentToolNode(tools))

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    workflow.add_edge("tools", "agent")

    return workflow.compile()


class LangGraphChatAgent(ChatAgent):
    def predict(
        self,
        messages: list[ChatAgentMessage],
        context: Optional[ChatContext] = None,
        custom_inputs: Optional[dict[str, Any]] = None,
    ) -> ChatAgentResponse:
        # Initialize agent in the predict call here
        agent = create_tool_calling_agent(llm, system_prompt)
        request = {"messages": self._convert_messages_to_dict(messages)}

        messages = []
        for event in agent.stream(request, stream_mode="updates"):
            for node_data in event.values():
                messages.extend(
                    ChatAgentMessage(**msg) for msg in node_data.get("messages", [])
                )
        return ChatAgentResponse(messages=messages)

    def predict_stream(
        self,
        messages: list[ChatAgentMessage],
        context: Optional[ChatContext] = None,
        custom_inputs: Optional[dict[str, Any]] = None,
    ) -> Generator[ChatAgentChunk, None, None]:
        agent = create_tool_calling_agent(llm, system_prompt)
        request = {"messages": self._convert_messages_to_dict(messages)}
        for event in agent.stream(request, stream_mode="updates"):
            for node_data in event.values():
                yield from (
                    ChatAgentChunk(**{"delta": msg}) for msg in node_data["messages"]
                )


# Create the agent object, and specify it as the agent object to use when
# loading the agent back for inference via mlflow.models.set_model()
AGENT = LangGraphChatAgent()
mlflow.models.set_model(AGENT)
