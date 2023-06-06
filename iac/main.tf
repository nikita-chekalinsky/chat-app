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
  source         = "./modules/security_groups"
  app_name       = var.app_name
  vpc_id         = module.vpc.vpc_id
  container_port = var.container_port
}

module "ecr" {
  source   = "./modules/ecr"
  app_name = var.app_name
}

/* module "alb" {
  source              = "./modules/alb"
  vpc_id              = module.vpc.vpc_id
  app_name            = var.app_name
  public_subnet_ids   = keys(module.vpc.public_subnets)
  private_subnet_ids  = keys(module.vpc.private_subnets)
  container_port      = var.container_port
  alb_security_groups = [module.security_groups.chat-app-sg.id]
} */



module "dynamodb" {
  source   = "./modules/dynamodb"
  app_name = var.app_name
}

output "access_key" {
  value     = module.dynamodb.dynamodb_user_access_key
  sensitive = true
}

output "access_secret" {
  value     = module.dynamodb.dynamodb_user_secret_key
  sensitive = true
}

