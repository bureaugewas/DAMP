INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO endpoints (name, endpoint_base, data, availability, status, author_id, created, valid_json, daily_rate_limit)
VALUES
  ('test name', '/api/fetch/test_name', 'test', 'Public', 'Active', 1, '2018-01-01 00:00:00', 0, 200),
  ('test name 2', '/api/fetch/test_name_2', 'test2' || x'0a' || 'data', 'Public', 'Active', 2, '2018-01-01 00:00:00', 0, 200);

INSERT INTO client_access (author_id, client_id, client_secret, endpoint_access_id, date_created, date_expiry, active,
  read_access, write_access, create_access, delete_access)
VALUES
  (1, 'test','pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
  1, '2018-01-01 00:00:00', '2118-01-01 00:00:00', 'TRUE', 'TRUE', 'TRUE', 'TRUE', 'TRUE');