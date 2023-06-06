resource "aws_dynamodb_table" "chats" {
  name     = "chats"
  hash_key = "chat_id"

  billing_mode                = "PAY_PER_REQUEST"
  deletion_protection_enabled = false
  point_in_time_recovery {
    enabled = false
  }

  attribute {
    name = "chat_id"
    type = "S"
  }
}
