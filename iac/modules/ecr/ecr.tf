locals {
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 1 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 1
      }
      action = {
        type = "expire"
      }
    }]
  })
}

resource "aws_ecr_repository" "notification_sender" {
  name                 = "notification-sender"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }

  tags = {
    Name = "notification-sender"
    App  = var.app_name
  }
}

resource "aws_ecr_lifecycle_policy" "notification_sender" {
  repository = aws_ecr_repository.notification_sender.name
  policy     = local.policy
}

