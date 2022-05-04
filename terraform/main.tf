resource "azurerm_resource_group" "rg" {
  name     = "rgSB-BROWNJL"
  location = "southcentralus"
  tags     = var.tags
}

resource "azurerm_mssql_server" "sql" {
  name                = "sqlcpcscus-brownjl"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  version             = "12.0"
  minimum_tls_version = "1.2"

  azuread_administrator {
    azuread_authentication_only = false
    login_username              = "AD-BROWNJL"
    object_id                   = var.ad-brownjl_object_id
  }

  tags = var.tags
}

resource "azurerm_mssql_firewall_rule" "sqlfw" {
  name             = "CPChem"
  server_id        = azurerm_mssql_server.sql.id
  start_ip_address = var.cpchem_ip_address
  end_ip_address   = var.cpchem_ip_address
}

resource "azurerm_mssql_elasticpool" "sqlep" {
  name                = "sqlepCPCscus-BROWNJL"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_mssql_server.sql.name
  max_size_gb         = 4.8828125

  sku {
    name     = "BasicPool"
    tier     = "Basic"
    capacity = 50
  }

  per_database_settings {
    min_capacity = 0
    max_capacity = 5
  }

  tags = var.tags
}

resource "azurerm_mssql_database" "sqldb" {
  name            = "sqldbCPCscus-BROWNJL"
  server_id       = azurerm_mssql_server.sql.id
  elastic_pool_id = azurerm_mssql_elasticpool.sqlep.id
  max_size_gb     = 1
  sku_name        = "ElasticPool"
  storage_account_type = "Local"
  zone_redundant = false

  tags = var.tags
}

resource "azurerm_key_vault" "kv" {
  name                        = "kvCPCscus-BROWNJL"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  enable_rbac_authorization   = true
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = true
  sku_name                    = "standard"

  tags = var.tags
}

resource "azurerm_role_assignment" "kvrbac" {
  scope                = azurerm_key_vault.kv.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = var.ad-brownjl_object_id
}