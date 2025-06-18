# Dais Demo

### Deployment Template
| DASF Control # | Details | Config Location | Terraform Resource Name |
|----------|----------|----------|----------|
| 1   | Single Sign-On with Multi-Factor Authentication    | Account Console > Settings    | N/A|


### Databricks AI Security Controls

#### Network Isolation
| DASF Control # | Details | Config Location | Terraform Resource Name |
|----------|----------|----------|----------|
| 1   | Single Sign-On with Multi-Factor Authentication    | Account Console > Settings    | N/A|
| 2   | Sync users and groups   | Account Console > User Management    |N/A|
| 3    | Restrict access w/ IP ACLs    | N/A   | databricks_ip_access_list | 
| 4    | Restrict access w/ private link     | [azure-dbx-dbfs-fw/main.tf](https://github.com/tonykhbo/dais25-dasf-demo/blob/master/azure-dbx-dbfs-fw/azure_dbx_infra/main.tf)| azurerm_databricks_workspace |
| 65    | Restrict outbound connections from models    | Account Console > Cloud Resources > [Network Policies](https://docs.databricks.com/aws/en/security/network/serverless-network-security/network-policies)  | N/A
| 62    | Implement network segmentation (NCC & PL)    | Account Console > Cloud Resources > [Network Connectivity Configurations](https://docs.databricks.com/aws/en/security/network/serverless-network-security/pl-to-internal-network)   | N/A


#### Guard against backdoor access
| DASF Control # | Details | Config Location | Terraform Resource Name |
|----------|----------|----------|----------|
| 62   | Encrypt data at rest with CMK    | [azure-dbx-dbfs-fw/main.tf](https://github.com/tonykhbo/dais25-dasf-demo/blob/master/azure-dbx-dbfs-fw/azure_dbx_infra/main.tf)   | azurerm_databricks_workspace | 
| 63   | Encrypt models  | Row 2    | | 

#### Least privilege access to data and AI
| DASF Control # | Details | Config Location | Terraform Resource Name |
|----------|----------|----------|----------|
| 5   | Control access to data     | Workspace > Unity Catalog > [Permissions](https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/ownership)   | N/A |
| 18  | Control access to models  | [Workspace > Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle/)  | N/A |
| 51    | Share data and AI assets securely    | Workspace > Unity Catalog > [Delta Sharing](https://docs.databricks.com/aws/en/delta-sharing/set-up)    | N/A |
| 57    | Use attribute-based access controls (ABAC)    | Unity Catalog > [Private Preview](https://docs.databricks.com/aws/en/data-governance/unity-catalog/abac/)   | N/A |
| 58    | Protect data w/ filters & masks    | Workspace > Unity Catalog > [Row filter](https://docs.databricks.com/aws/en/tables/row-and-column-filters#apply-a-row-filter) / [Mask](https://docs.databricks.com/aws/en/tables/row-and-column-filters#apply-a-column-mask)     | N/A |
| 64    | Limit access from AI models and agents (OBO)    | Workspace > Unity Catalog > Permissions    | N/A |


#### AI guardrails
| DASF Control # | Details | Config Location | Terraform Resource Name |
|----------|----------|----------|----------|
| 37   | Implement Input & output AI guardrails    | Workspace > Serving > [AI Gateway](https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints)   | N/A
| 54   | Streamline the usage and management of various large language model (LLM) providers  | Workspace > Serving   | N/A
| 55   | Set up inference tables to monitor and debug models  | Workspace > Serving > [AI Gateway](https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints)    | N/A
| 60   | Rate limit number of inference queries  | Workspace > Serving > [AI Gateway](https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints)    | N/A
