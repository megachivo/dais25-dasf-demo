# Databricks notebook source
# MAGIC %md # Vector Search Python SDK example usage
# MAGIC
# MAGIC This notebook shows how to use the Vector Search Python SDK, which provides a `VectorSearchClient` as a primary API for working with Vector Search.
# MAGIC
# MAGIC Alternatively, you can call the REST API directly.
# MAGIC
# MAGIC ## Requirements
# MAGIC
# MAGIC This notebook assumes that a Model Serving endpoint named `databricks-bge-large-en` exists. To create that endpoint, see the "Vector Search foundational embedding model (BGE) Example" notebook ([AWS](https://docs.databricks.com/en/generative-ai/create-query-vector-search.html#call-a-bge-embeddings-model-using-databricks-model-serving-notebook)|[Azure](https://learn.microsoft.com/en-us/azure/databricks/generative-ai/create-query-vector-search#call-a-bge-embeddings-model-using-databricks-model-serving-notebook)).

# COMMAND ----------

# MAGIC %pip install --upgrade --force-reinstall databricks-vectorsearch
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

from databricks.vector_search.client import VectorSearchClient

vsc = VectorSearchClient()

# COMMAND ----------

help(VectorSearchClient)

# COMMAND ----------

# MAGIC %md ## Load toy dataset into source Delta table

# COMMAND ----------

# MAGIC %md
# MAGIC The following creates the source Delta table.

# COMMAND ----------


# Specify the catalog and schema to use. You must have USE_CATALOG privilege on the catalog and USE_SCHEMA and CREATE_TABLE privileges on the schema.
# Change the catalog and schema here if necessary.

catalog_name = "dasf"
schema_name = "ai_demo"


# COMMAND ----------

source_table_name = "employees_details"
source_table_fullname = f"{catalog_name}.{schema_name}.{source_table_name}"

# COMMAND ----------

# Uncomment if you want to start from scratch.
spark.sql(f"DROP TABLE IF EXISTS {source_table_fullname}")

# COMMAND ----------

#source_df = spark.read.parquet("/databricks-datasets/wikipedia-datasets/data-001/en_wikipedia/articles-only-parquet").limit(10)
source_df = spark.sql("SELECT * FROM dasf.ai_demo.employees").limit(100)
display(source_df)

# COMMAND ----------

source_df.write.format("delta").option("delta.enableChangeDataFeed", "true").saveAsTable(source_table_fullname)

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {source_table_fullname}"))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Create vector search endpoint

# COMMAND ----------

vector_search_endpoint_name = "vector-search-demo-endpoint"

# COMMAND ----------

try:
    vsc.create_endpoint(
        name=vector_search_endpoint_name,
        endpoint_type="STANDARD"
    )
except Exception as e:
    print(e)

# COMMAND ----------

endpoint = vsc.get_endpoint(
  name=vector_search_endpoint_name)
endpoint

# COMMAND ----------

# MAGIC %md ## Create vector index

# COMMAND ----------

# Vector index
vs_index = "employee_index"
vs_index_fullname = f"{catalog_name}.{schema_name}.{vs_index}"

embedding_model_endpoint = "databricks-bge-large-en"

# COMMAND ----------

index = vsc.create_delta_sync_index(
  endpoint_name=vector_search_endpoint_name,
  source_table_name=source_table_fullname,
  index_name=vs_index_fullname,
  pipeline_type='TRIGGERED',
  primary_key="employee_id",
  embedding_source_column="description",
  embedding_model_endpoint_name=embedding_model_endpoint
)
index.describe()

# COMMAND ----------

# MAGIC %md ## Get a vector index  
# MAGIC
# MAGIC Use `get_index()` to retrieve the vector index object using the vector index name. You can also use `describe()` on the index object to see a summary of the index's configuration information.

# COMMAND ----------



index = vsc.get_index(endpoint_name=vector_search_endpoint_name, index_name=vs_index_fullname)

index.describe()

# COMMAND ----------

# Wait for index to come online. Expect this command to take several minutes.
import time
while not index.describe().get('status').get('detailed_state').startswith('ONLINE'):

 print("Waiting for index to be ONLINE...")
 time.sleep(5)
print("Index is ONLINE")
index.describe()

# COMMAND ----------

# MAGIC %md ## Similarity search
# MAGIC
# MAGIC Query the Vector Index to find similar documents.

# COMMAND ----------

# Returns [col1, col2, ...]
# You can set this to any subset of the columns.
all_columns = spark.table(source_table_fullname).columns

results = index.similarity_search(
  query_text="junior developer",
  columns=all_columns,
  num_results=2)

results

# COMMAND ----------

# Search with a filter.
results = index.similarity_search(
  query_text="*",
  columns=all_columns,
  filters={"employee_id": ("10", "11")},
  num_results=2)

results


# COMMAND ----------

# MAGIC %md ## Convert results to LangChain documents
# MAGIC
# MAGIC The first column retrieved is loaded into `page_content`, and the rest into metadata.

# COMMAND ----------

# You must have langchain installed on your cluster. The following command installs or upgrades langchain.
%pip install --upgrade langchain
