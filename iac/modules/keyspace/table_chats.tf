/* resource "aws_keyspaces_table" "chats" {
  keyspace_name = aws_keyspaces_keyspace.chat_app.name
  table_name    = "chats"

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
      name = "chat_id"
      type = "uuid"
    }
    column {
      name = "name"
      type = "text"
    }
    column {
      name = "user_ids"
      type = "list<uuid>"
    }
    partition_key {
      name = "chat_id"
    }
  }
} */
