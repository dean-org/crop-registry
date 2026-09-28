INSERT INTO "public"."approval_stage" ("id","policy_id","stage_order","name","mode","mode_value","sla_hours","parallel_group","skip_if","on_empty","on_breach","escalation_rules_json","created_at","updated_at")
SELECT v."id", v."policy_id", v."stage_order"::int, v."name", v."mode", v."mode_value"::int, v."sla_hours"::int,
       v."parallel_group"::int, v."skip_if"::json, v."on_empty", v."on_breach", v."escalation_rules_json"::json,
       v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('3491e79c-35f5-5c0d-ae21-97abc966cefe', 'bafaf455-c497-5605-b9e1-3673ffd0cfc0', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('5eab72fd-6e5e-5c42-8e92-981a71bb5cdc', 'bafaf455-c497-5605-b9e1-3673ffd0cfc0', 2, 'Stage 2 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('c56a1f07-7345-5a54-b00e-9b07d0722d0c', 'fd5b3e7e-c25f-5ecd-af18-2a76a6b57a92', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('fd96bca5-583e-53b7-846a-cb1dd9384009', 'fd5b3e7e-c25f-5ecd-af18-2a76a6b57a92', 2, 'Stage 2 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW())
) AS v("id","policy_id","stage_order","name","mode","mode_value","sla_hours","parallel_group","skip_if","on_empty","on_breach","escalation_rules_json","created_at","updated_at")
WHERE EXISTS (SELECT 1 FROM "public"."approval_policy" p WHERE p.id = v."policy_id")
ON CONFLICT DO NOTHING;
