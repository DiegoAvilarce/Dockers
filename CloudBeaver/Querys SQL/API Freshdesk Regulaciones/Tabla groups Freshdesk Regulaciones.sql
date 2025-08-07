CREATE TABLE api_freshdesk_regulaciones.groups(
  id BIGINT,
  name VARCHAR(255),
  description TEXT,
  escalate_to BIGINT,
  unassigned_for TEXT,
  business_hour_id BIGINT,
  group_type VARCHAR(50),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  auto_ticket_assign INT,
  timestamp_nifi TIMESTAMPTZ,
  PRIMARY KEY (id)
);