terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "d33b95c7-af3c-4247-9661-aa96d47fccc0"
}

data "azurerm_resource_group" "main" {
  name     = "Cohort31_MicHor_ProjectExercise"
}

resource "azurerm_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "main" {
  name                = "mrh-todoapp12"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker_image_name     = "michaelsminis/todo-app:latest"
      docker_registry_url   = "https://docker.io"
    }
  }
}




resource "azurerm_cosmosdb_account" "main" {
  name                  = "mrhtodoapp"
  location              = data.azurerm_resource_group.main.location
  resource_group_name   = data.azurerm_resource_group.main.name
  offer_type            = "Standard"
  kind                  = "MongoDB"

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
      name = "EnableServerless"
  }

  consistency_policy {
    consistency_level = "Strong"
  }

  geo_location {
    location          = "uk south"
    failover_priority = 0
  }

}


data "azurerm_cosmosdb_account" "main" {
  name                = "mrhtodoapp"
  resource_group_name = "Cohort31_MicHor_ProjectExercise"
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "mrhtodoappdb"
  resource_group_name = data.azurerm_cosmosdb_account.main.resource_group_name
  account_name        = data.azurerm_cosmosdb_account.main.name
  throughput          = 400
    lifecycle { prevent_destroy = true }
}
