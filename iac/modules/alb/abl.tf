resource "aws_lb" "notification-sender-alb" {
  name               = "notification-sender-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = var.alb_security_groups
  subnets            = var.public_subnet_ids
  idle_timeout       = 4000

  tags = {
    Name = "notification-sender-alb"
    App  = var.app_name
  }
}


resource "aws_lb_listener" "notification-sender-alb-listener" {
  load_balancer_arn = aws_lb.notification-sender-alb.arn
  port              = var.container_port
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.notification-sender-alb-tg.arn
  }
}

