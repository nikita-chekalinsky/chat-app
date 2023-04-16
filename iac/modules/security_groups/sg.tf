resource "aws_security_group" "chat-app-sg" {
  name        = "chat-app-sg"
  description = "Allow inbound traffic from the internet"
  vpc_id      = var.vpc_id

  ingress {
    description      = "Allow HTTP traffic"
    from_port        = var.container_port
    to_port          = var.container_port
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "chat-app-sg"
  }
}

output "chat-app-sg" {
  value = aws_security_group.chat-app-sg
}
