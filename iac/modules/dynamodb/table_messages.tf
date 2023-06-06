resource "aws_dynamodb_table" "messages" {
  name      = "messages"
  hash_key  = "chat_id"
  range_key = "message_timestamp"

  billing_mode                = "PAY_PER_REQUEST"
  deletion_protection_enabled = false
  point_in_time_recovery {
    enabled = false
  }

  attribute {
    name = "chat_id"
    type = "S"
  }
  attribute {
    name = "message_timestamp"
    type = "S"
  }
}

