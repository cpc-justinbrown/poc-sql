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
    azuread_authentication_only = true
    login_username              = "AD-BROWNJL"
    object_id                   = "268f5e47-eb76-485b-a9fb-59a68d444af3"
  }

  tags = var.tags
}

resource "azurerm_mssql_firewall_rule" "sqlfw" {
  name             = "CPChem"
  server_id        = azurerm_mssql_server.sql.id
  start_ip_address = "64.129.107.15"
  end_ip_address   = "64.129.107.15"
}

resource "azurerm_mssql_elasticpool" "sqlep" {
  name                = "sqlepCPCscus-BROWNJL"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  server_name         = azurerm_mssql_server.sql.name
  license_type        = "LicenseIncluded"
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
}