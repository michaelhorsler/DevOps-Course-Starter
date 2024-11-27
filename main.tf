terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
      resource_group_name  = "Cohort31_MicHor_ProjectExercise"
      storage_account_name = "mrhtodoappstorage"
      container_name       = "mrhtodoappcontainer"
      key                  = "terraform.tfstate"
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
  app_settings = {
    "FLASK_APP" = var.FLASK_APP
    "FLASK_DEBUG" = var.FLASK_DEBUG
    "MONGO_CONN_STRING" = var.MONGO_CONN_STRING
    "MONGODB" = var.MongoDB
    "SECRET_KEY" = var.SECRET_KEY
    "OAUTH_CLIENT_ID" = var.OAUTH_CLIENT_ID
    "OAUTH_CLIENT_SECRET" = var.OAUTH_CLIENT_SECRET
  }
}


resource "azurerm_cosmosdb_account" "main" {
  name                  = "mrhtodoapp"
  location              = data.azurerm_resource_group.main.location
  resource_group_name   = data.azurerm_resource_group.main.name
  offer_type            = "Standard"
  kind                  = "MongoDB"
  mongo_server_version  = "4.2"
    lifecycle { prevent_destroy = true }

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
}
