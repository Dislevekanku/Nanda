-- Demo data for MedSpa Agent
INSERT INTO account (id, name) VALUES (1, 'Glow MedSpa') ON CONFLICT DO NOTHING;

INSERT INTO staff (id, account_id, email, first_name, last_name, role, password_hash, is_active)
VALUES
    (1, 1, 'alex@glowmedspa.com', 'Alex', 'Rivera', 'provider', '390000$Z2xvd21lZHNwYXNhbHQhIQ==$Sh9IeuluKYCohAqM4wo3Hp9lzweFOHaM50fUWWywp+M=', true),
    (2, 1, 'jamie@glowmedspa.com', 'Jamie', 'Lee', 'provider', '390000$Z2xvd21lZHNwYXNhbHQhIQ==$Sh9IeuluKYCohAqM4wo3Hp9lzweFOHaM50fUWWywp+M=', true),
    (3, 1, 'morgan@glowmedspa.com', 'Morgan', 'Smith', 'provider', '390000$Z2xvd21lZHNwYXNhbHQhIQ==$Sh9IeuluKYCohAqM4wo3Hp9lzweFOHaM50fUWWywp+M=', true)
ON CONFLICT DO NOTHING;

INSERT INTO service (id, account_id, name, description, duration_minutes, price_cents)
VALUES
    (1, 1, 'Botox', 'Personalized Botox treatment', 30, 35000),
    (2, 1, 'HydraFacial', 'Hydrating facial treatment', 45, 22500),
    (3, 1, 'Dermal Fillers', 'Targeted filler service', 60, 45000),
    (4, 1, 'Microneedling', 'Skin rejuvenation session', 50, 32000),
    (5, 1, 'Chemical Peel', 'Brightening chemical peel', 40, 28000)
ON CONFLICT DO NOTHING;

INSERT INTO client (id, account_id, email, first_name, last_name, phone_number)
VALUES
    (1, 1, 'pat@example.com', 'Pat', 'Taylor', '+15550000001'),
    (2, 1, 'taylor@example.com', 'Taylor', 'Morgan', '+15550000002'),
    (3, 1, 'skyler@example.com', 'Skyler', 'Jordan', '+15550000003')
ON CONFLICT DO NOTHING;
