CREATE KEYSPACE IF NOT EXISTS chat_app 
WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE chat_app;


CREATE TABLE IF NOT EXISTS chat_app.users (
    user_id uuid,
    username text,
    chat_ids set<uuid>,
    PRIMARY KEY (user_id)
);


CREATE TABLE IF NOT EXISTS chat_app.chats (
    chat_id uuid,
    name text,
    user_ids set<uuid>,
    PRIMARY KEY (chat_id)
);


CREATE TABLE IF NOT EXISTS chat_app.messages (
    chat_id uuid,
    message_timestamp timestamp,
    message_text text,
    sender_id uuid,
    attachment_links set<text>,
    PRIMARY KEY ((chat_id), message_timestamp)
) WITH CLUSTERING ORDER BY (message_timestamp DESC)
