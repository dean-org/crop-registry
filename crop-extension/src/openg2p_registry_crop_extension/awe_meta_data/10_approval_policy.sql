INSERT INTO "public"."approval_policy" ("id","policy_key","version","name","description","status","artifact_type","created_by","forbid_self_approval","forbid_repeat_approvers","created_at","updated_at") VALUES
    ('bafaf455-c497-5605-b9e1-3673ffd0cfc0', 'registry.change_request.crop', 1, 'Policy for Crop Change Request', NULL, 'active', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('fd5b3e7e-c25f-5ecd-af18-2a76a6b57a92', 'registry.intake_form.crop', 1, 'Policy for Crop Intake Form', NULL, 'active', 'registry.intake_form', 'seed', 'FALSE', 'FALSE', NOW(), NOW())
-- Untargeted DO NOTHING: approval_policy also has uq_policy_key_version; targeting "id" alone would leave
-- a natural-key clash unguarded and abort the whole statement.
ON CONFLICT DO NOTHING;
