variable "app_name" {
  type = string
}

variable "cidr" {
  type    = string
  default = "10.0.0.0/20"
}

variable "public_subnet" {
  type = map(string)

  description = "Map of public subnets"

  default = {
    "ap-northeast-1a" = "10.0.0.0/24"
    "ap-northeast-1b" = "10.0.32.0/24"
  }
}

variable "privete_subnet" {
  type = map(string)

  description = "Map of private subnets"

  default = {
    "ap-northeast-1a" = "10.0.64.0/24"
    "ap-northeast-1b" = "10.0.96.0/24"
  }
}
