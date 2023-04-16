provider "aws" {
  region = var.aws_region
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.63.0"
    }
  }
}

module "vpc" {
  source   = "./modules/vpc"
  app_name = var.app_name
}
