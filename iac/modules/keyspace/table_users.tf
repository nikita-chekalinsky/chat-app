/* resource "aws_keyspaces_table" "users" {
  keyspace_name = aws_keyspaces_keyspace.chat_app.name
  table_name    = "users"

  capacity_specification {
    throughput_mode      = "PAY_PER_REQUEST"
    read_capacity_units  = 1
    write_capacity_units = 1
  }

  point_in_time_recovery {
    status = "DISABLED"
  }

  schema_definition {
    column {
      name = "user_id"
      type = "uuid"
    }
    column {
      name = "username"
      type = "text"
    }
    column {
      name = "password"
      type = "text"
    }
    column {
      name = "email"
      type = "text"
    }
    column {
      name = "chat_ids"
      type = "list<uuid>"
    }
    partition_key {
      name = "user_id"
    }
  }
} */
