CREATE TABLE api_freshdesk_sistemas.ticket_fields_choices (
  id BIGINT,
  id_ticket_fields BIGINT,
  name_field VARCHAR(255),
  label VARCHAR(255),
  label_for_customers VARCHAR(255),
  value VARCHAR(255),
  position INT,
  default_ BOOLEAN,
  stop_sla_timer BOOLEAN,
  deleted BOOLEAN,
  group_ids TEXT,
  timestamp_nifi TIMESTAMPTZ,
  PRIMARY KEY (id_ticket_fields,label,value)
);