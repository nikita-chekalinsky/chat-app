resource "aws_vpc" "chat-app-vpc" {
  cidr_block = var.cidr

  tags = {
    app = var.app_name
  }
}

output "vpc_id" {
  value = aws_vpc.chat-app-vpc.id
}
