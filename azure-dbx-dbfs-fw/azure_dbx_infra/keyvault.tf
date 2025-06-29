
# =========================
# BEGIN: Azure Key Vault Section
# =========================



resource "azurerm_key_vault" "this" {


  name                     = "${var.prefix}-${random_string.test.result}-kv"
  location                 = azurerm_resource_group.resourcegroup.location
  resource_group_name      = azurerm_resource_group.resourcegroup.name
  tenant_id                = data.azurerm_client_config.current.tenant_id
  purge_protection_enabled = true

  sku_name                   = "premium"
  soft_delete_retention_days = 7


}

# Define a key in the Azure Key Vault for managed services
resource "azurerm_key_vault_key" "managed_services" {
  

  name         = "${var.prefix}-${random_string.test.result}-adb-services"
  key_vault_id = azurerm_key_vault.this.id
  key_type     = "RSA"
  key_size     = 2048

  key_opts = [
    "decrypt",
    "encrypt",
    "sign",
    "unwrapKey",
    "verify",
    "wrapKey",
  ]


  depends_on = [azurerm_key_vault_access_policy.terraform]
}

# Define a key in the Azure Key Vault for managed disks
resource "azurerm_key_vault_key" "managed_disk" {
 

  name         = "${var.prefix}-${random_string.test.result}-adb-disk"
  key_vault_id = azurerm_key_vault.this.id
  key_type     = "RSA"
  key_size     = 2048

  key_opts = [
    "decrypt",
    "encrypt",
    "sign",
    "unwrapKey",
    "verify",
    "wrapKey",
  ]


  depends_on = [azurerm_key_vault_access_policy.terraform]
}

# Define an access policy for the Azure Key Vault
resource "azurerm_key_vault_access_policy" "terraform" {
 

  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = azurerm_key_vault.this.tenant_id
  object_id    = data.azurerm_client_config.current.object_id

  key_permissions = [
    "Get",
    "List",
    "Create",
    "Decrypt",
    "Encrypt",
    "Sign",
    "UnwrapKey",
    "Verify",
    "WrapKey",
    "Delete",
    "Restore",
    "Recover",
    "Update",
    "Purge",
    "GetRotationPolicy"
  ]
}

resource "azurerm_key_vault_access_policy" "databricks" {
 

  key_vault_id = azurerm_key_vault.this.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azuread_service_principal.this.object_id
  key_permissions = [
    "Get",
    "UnwrapKey",
    "WrapKey",
  ]
}

resource "azurerm_private_dns_zone" "key_vault" {


  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = azurerm_resource_group.resourcegroup.name

 
}

resource "azurerm_private_endpoint" "key_vault" {


  name                = "${var.prefix}-${random_string.test.result}-kv-pep"
  location            = azurerm_resource_group.resourcegroup.location
  resource_group_name = azurerm_resource_group.resourcegroup.name
  subnet_id           = azurerm_subnet.plsubnet.id

  private_service_connection {
    name                           = "keyvault"
    private_connection_resource_id = azurerm_key_vault.this.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }

  private_dns_zone_group {
    name                 = "keyvault"
    private_dns_zone_ids = [azurerm_private_dns_zone.key_vault.id]
  }


}

resource "azurerm_private_dns_zone_virtual_network_link" "key_vault" {
 

  name                  = "${var.prefix}-${random_string.test.result}-keyvault-vnetlink"
  resource_group_name   = azurerm_resource_group.resourcegroup.name
  private_dns_zone_name = azurerm_private_dns_zone.key_vault.name
  virtual_network_id    = azurerm_virtual_network.vnet_for_databricks.id

 
}

# =========================
# END: Azure Key Vault Section
# =========================
