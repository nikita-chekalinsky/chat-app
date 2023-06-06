variable "app_name" {
  description = "The name of the application"
  default     = "chat-app"
  type        = string
}

variable "public_subnet_ids" {
  description = "The public subnets to deploy to"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "The private subnets to deploy to"
  type        = list(string)
}

variable "vpc_id" {
  description = "The VPC to deploy to"
  type        = string
}

variable "alb_security_groups" {
  description = "The security group to deploy to"
  type        = list(string)
}

variable "health_check_path" {
  description = "The health check path"
  type        = string
  default     = "/health"
}

variable "container_port" {
  type        = number
  description = "The port the container is listening on"
}
