resource "aws_dynamodb_table" "users" {
  name     = "users"
  hash_key = "user_id"

  billing_mode                = "PAY_PER_REQUEST"
  deletion_protection_enabled = false
  point_in_time_recovery {
    enabled = false
  }


  attribute {
    name = "user_id"
    type = "S"
  }
}
