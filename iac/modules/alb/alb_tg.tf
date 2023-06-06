resource "aws_lb_target_group" "notification-sender-alb-tg" {
  name        = "notification-sender-tg"
  port        = var.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = "/"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = {
    Name = "notification-sender-tg"
    App  = var.app_name
  }
}
