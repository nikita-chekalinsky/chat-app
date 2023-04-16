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

module "security_groups" {
  source   = "./modules/security_groups"
  app_name = var.app_name
  vpc_id   = module.vpc.vpc_id
}

module "ecr" {
  source   = "./modules/ecr"
  app_name = var.app_name
}
