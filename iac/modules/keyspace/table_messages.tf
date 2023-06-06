resource "aws_keyspaces_table" "messages" {
  keyspace_name = aws_keyspaces_keyspace.chat_app.name
  table_name    = "messages"

  capacity_specification {
    throughput_mode = "PAY_PER_REQUEST"
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
      name = "message_text"
      type = "text"
    }
    column {
      name = "sender_id"
      type = "uuid"
    }
    column {
      name = "message_timestamp"
      type = "timestamp"
    }
    column {
      name = "attachment_links"
      type = "list<text>"
    }

    partition_key {
      name = "chat_id"
    }
  }
}
