INSERT INTO "public"."approver_rule" ("id","stage_id","rule_type","rule_value","kind","required","created_at","updated_at")
SELECT v."id", v."stage_id", v."rule_type", v."rule_value"::json, v."kind", v."required"::boolean,
       v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('ee2216c1-890a-5dd2-ae55-06cad86b3546', '3491e79c-35f5-5c0d-ae21-97abc966cefe', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('d0a5c4ae-1dc6-520f-9c56-68748317236a', '5eab72fd-6e5e-5c42-8e92-981a71bb5cdc', 'user', '{"user_id": "nina.patel"}', 'approver', 'FALSE', NOW(), NOW()),
    ('0cf3656d-f82e-56ba-991d-1dfc00554c7d', 'c56a1f07-7345-5a54-b00e-9b07d0722d0c', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('65cb976d-3ac0-5e9c-bf87-9c1f8d4ba887', 'fd96bca5-583e-53b7-846a-cb1dd9384009', 'user', '{"user_id": "nina.patel"}', 'approver', 'FALSE', NOW(), NOW())
) AS v("id","stage_id","rule_type","rule_value","kind","required","created_at","updated_at")
WHERE EXISTS (SELECT 1 FROM "public"."approval_stage" s WHERE s.id = v."stage_id")
ON CONFLICT DO NOTHING;
