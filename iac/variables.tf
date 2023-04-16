variable "app_name" {
  description = "The name of the application"
  default     = "chat-app"
  type        = string
}

variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "ap-northeast-1"
}
