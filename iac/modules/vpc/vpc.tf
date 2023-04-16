resource "aws_vpc" "chat-app-vpc" {
  cidr_block = var.cidr


  tags = {
    app  = var.app_name
    Name = "chat-app-vpc"
  }
}

output "vpc_id" {
  value = aws_vpc.chat-app-vpc.id
}


resource "aws_subnet" "chat-app-public-subnet" {
  for_each = var.public_subnet

  vpc_id            = aws_vpc.chat-app-vpc.id
  availability_zone = each.key
  cidr_block        = each.value
  tags = {
    app  = var.app_name
    Name = "chat-app-public-subnet-${each.key}"
  }
}

output "public_subnets" {
  value = {
    for subnet in aws_subnet.chat-app-public-subnet : subnet.id => subnet.cidr_block
  }
}

resource "aws_subnet" "chat-app-private-subnet" {
  for_each = var.privete_subnet

  vpc_id            = aws_vpc.chat-app-vpc.id
  availability_zone = each.key
  cidr_block        = each.value
  tags = {
    app  = var.app_name
    Name = "chat-app-private-subnet-${each.key}"
  }
}

output "private_subnets" {
  value = {
    for subnet in aws_subnet.chat-app-private-subnet : subnet.id => subnet.cidr_block
  }
}
