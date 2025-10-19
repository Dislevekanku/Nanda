-- Example row level security policies for Supabase/Postgres
ALTER TABLE account ENABLE ROW LEVEL SECURITY;
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;
ALTER TABLE service ENABLE ROW LEVEL SECURITY;
ALTER TABLE client ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointment ENABLE ROW LEVEL SECURITY;
ALTER TABLE convo ENABLE ROW LEVEL SECURITY;
ALTER TABLE message ENABLE ROW LEVEL SECURITY;
ALTER TABLE automation_event ENABLE ROW LEVEL SECURITY;

-- Row filter on account_id
CREATE POLICY account_isolation ON service
    USING (account_id = current_setting('app.current_account')::INT);

CREATE POLICY account_isolation_client ON client
    USING (account_id = current_setting('app.current_account')::INT);

CREATE POLICY account_isolation_appointment ON appointment
    USING (account_id = current_setting('app.current_account')::INT);

CREATE POLICY account_isolation_convo ON convo
    USING (account_id = current_setting('app.current_account')::INT);

-- Only staff or service bots can access messages
CREATE POLICY message_access_policy ON message
    USING (
        current_setting('app.current_role', true) IN ('staff', 'service_bot')
    );
