DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS endpoints;
DROP TABLE IF EXISTS client_access;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE endpoints (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  name TEXT UNIQUE NOT NULL,
  availability TEXT NOT NULL default 'Private',
  status TEXT NOT NULL,
  endpoint_base TEXT UNIQUE NOT NULL,
  tags TEXT,
  data TEXT NOT NULL,
  valid_json BOOL NOT NULL,
  daily_rate_limit INTEGER DEFAULT 200,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE client_access (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  client_id TEXT UNIQUE NOT NULL,
  client_secret TEXT UNIQUE NOT NULL,
  endpoint_access_id INTEGER NOT NULL,
  date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_expiry TIMESTAMP NOT NULL ,
  active BOOL NOT NULL DEFAULT 'TRUE',
  read_access BOOL NOT NULL DEFAULT 'FALSE',
  write_access BOOL NOT NULL DEFAULT 'FALSE',
  create_access BOOL NOT NULL DEFAULT 'FALSE',
  delete_access BOOL NOT NULL DEFAULT 'FALSE',
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (endpoint_access_id) REFERENCES endpoints (id)
);