# Dais Demo

#### Network Isolation
| DASF Control # | Details | Config Location | Terraform Resource Name |
|----------|----------|----------|----------|
| 1   | Single Sign-On with Multi-Factor Authentication    | Account Console > Settings    | N/A|
| 2   | Sync users and groups   | Account Console > User Management    |N/A|
| 3    | Restrict access w/ IP ACLs    | N/A   | databricks_ip_access_list | 
| 4    | Restrict access w/ private link     | [azure-dbx-dbfs-fw/main.tf](https://github.com/tonykhbo/dais25-dasf-demo/blob/master/azure-dbx-dbfs-fw/azure_dbx_infra/main.tf)| azurerm_databricks_workspace |
| 65    | Restrict outbound connections from models    | Account Console > Cloud Resources > Network Policies  | N/A
| 62    | Implement network segmentation (NCC & PL)    | Account Console > Cloud Resources > Network Connectivity Configurations   | N/A


#### Guard against backdoor access
| DASF Control # | Details | Configuration |
|----------|----------|----------|
| 62   | Encrypt data at rest with CMK    | Row 1    |
| 63   | Encrypt models  | Row 2    |

#### Least privilege access to data and AI
| DASF Control # | Details | Configuration |
|----------|----------|----------|
| 5   | Control access to data     | Row 1    |
| 18  | Control access to models  | Row 2    |
| 51    | Share data and AI assets securely    | Row 3    |
| 57    | Use attribute-based access controls (ABAC)    | Row 3    |
| 58    | Protect data w/ filters & masks    | Row 3    |
| 64    | Limit access from AI models and agents (OBO)    | Row 3    |


#### AI guardrails
| DASF Control # | Details | Configuration |
|----------|----------|----------|
| 37   | Implement Input & output AI guardrails    | Row 1    |
| 54   | Streamline the usage and management of various large language model (LLM) providers  | Row 2    |
| 55   | Set up inference tables to monitor and debug models  | Row 2    |
| 60   | Rate limit number of inference queries  | Row 2    |
