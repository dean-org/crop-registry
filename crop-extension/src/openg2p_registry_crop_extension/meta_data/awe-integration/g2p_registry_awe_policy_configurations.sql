INSERT INTO "public"."g2p_registry_awe_policy_configurations" ("awe_policy_config_id","policy_scope","register_id","intake_form_id","section_id","policy_type","policy_key","context_field_names") VALUES
    ('ac61bdcf-2ef7-5670-b723-5362d35e68a9', 'REGISTER', '9ce1fa5a-d86e-55aa-be65-529182866b0c', '', '', 'registry.change_request', 'registry.change_request.crop', 'null'),
    ('860d2966-6d07-51bf-8741-85385fbb0957', 'INTAKE_FORM', '9ce1fa5a-d86e-55aa-be65-529182866b0c', 'e0e9caec-af10-5dd0-94ee-bdecdbd807f5', '', 'registry.intake_form', 'registry.intake_form.crop', 'null')
ON CONFLICT ("awe_policy_config_id") DO NOTHING;
