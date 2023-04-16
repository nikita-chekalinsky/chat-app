resource "aws_internet_gateway" "chat-app-igw" {
  vpc_id = aws_vpc.chat-app-vpc.id

  tags = {
    app = var.app_name
  }
}

output "igw_id" {
  value = aws_internet_gateway.chat-app-igw.id
}
