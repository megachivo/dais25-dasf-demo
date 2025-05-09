terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.114.0"
    }
    random = {
      source = "hashicorp/random"
    }
  }
}

provider "random" {
}

provider "azurerm" {
  features {}
  subscription_id = "3f2e4d32-8e8d-46d6-82bc-5bb8d962328b"
}
