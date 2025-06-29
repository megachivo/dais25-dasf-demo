# variable resource_group_name {
#   description = "The name of the resource group in which to create the Databricks workspace."
#   type        = string
# }

# variable databricks_workspace_name {
#   description = "The name of the Databricks workspace."
#   type        = string
# }

# variable managed_rg {
#   description = "The name of the managed resource group in which to create the Databricks workspace."
#   type        = string
# }

# variable ws_managed_storage_account_name {
#   description = "The name of the storage account in which to create the Databricks workspace."
#   type        = string
# }

variable location { 
  description = "The location/region where the Databricks workspace should be created."
  type        = string
}

variable prefix {
  description = "Prefix for locations and other resources that are labeled consistenly for networking"
  type        = string
}

variable cidr {
  description = "The CIDR range for the network that we will be provisioning"
  type        = string
}

variable email {
  description = "For tagging the RG"
  type        = string
}

variable remove_date {
  description = "For tagging the RG"
  type        = string
}

variable description {
  description = "For tagging the RG"
  type        = string
}

variable "client_config" {
  description = "Client configuration object containing tenant_id and other properties."
  type = object({
    tenant_id = string
    object_id = string
  })
}


# Get the current client config for tenant and object id
data "azurerm_client_config" "current" {
}

# Get the Azure DataBricks service principal object id
data "azuread_application_published_app_ids" "well_known" {}

# Get the object id of the Azure DataBricks service principal
data "azuread_service_principal" "this" {
  client_id = data.azuread_application_published_app_ids.well_known.result["AzureDataBricks"]
}
