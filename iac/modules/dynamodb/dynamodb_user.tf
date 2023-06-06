resource "aws_iam_user" "dynamodb_user" {
  name = "dynamodb_user"
}

resource "aws_iam_access_key" "dynamodb_user" {
  user = aws_iam_user.dynamodb_user.name
}

resource "aws_iam_user_policy_attachment" "dynamodb_policy_attachment" {
  user       = aws_iam_user.dynamodb_user.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

output "dynamodb_user_access_key" {
  value = aws_iam_access_key.dynamodb_user.id
}

output "dynamodb_user_secret_key" {
  value = aws_iam_access_key.dynamodb_user.secret
}
