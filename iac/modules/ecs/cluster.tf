resource "aws_ecs_cluster" "chat-app-cluster" {
  name = "chat-app-cluster"
  tags = {
    App  = var.app_name
    Name = "chat-app-cluster"
  }
}
