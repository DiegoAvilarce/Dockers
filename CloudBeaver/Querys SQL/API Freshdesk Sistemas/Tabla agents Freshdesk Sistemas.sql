CREATE TABLE api_freshdesk_sistemas.agents(
  id BIGINT,
  available BOOLEAN,
  occasional BOOLEAN,
  ticket_scope INT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  last_active_at TIMESTAMP,
  available_since TEXT,
  type VARCHAR(50),
  contact JSONB,
  deactivated BOOLEAN,
  signature TEXT,
  focus_mode BOOLEAN,
  timestamp_nifi TIMESTAMPTZ,
  PRIMARY KEY (id)
  );