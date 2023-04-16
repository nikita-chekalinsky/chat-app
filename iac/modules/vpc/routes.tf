resource "aws_route_table" "chat-app-public-route-table" {
  vpc_id = aws_vpc.chat-app-vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.chat-app-igw.id
  }

  tags = {
    app  = var.app_name
    Name = "chat-app-public-route-table"
  }
}

resource "aws_route_table_association" "chat-app-public-route-table-association" {
  for_each = aws_subnet.chat-app-public-subnet

  subnet_id      = each.value.id
  route_table_id = aws_route_table.chat-app-public-route-table.id
}

output "public_route_table_id" {
  value = aws_route_table.chat-app-public-route-table.id
}
