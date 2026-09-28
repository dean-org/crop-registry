-- Default code lists for the Crop Registry. DEFAULTS, not a definition: a country pack loaded by
-- load_attributes_from_mds replaces any list with the same attribute_id, and an admin can edit them.

INSERT INTO "public"."g2p_attributes" ("attribute_id","attribute_code","attribute_display","is_hierarchical") VALUES 
('CROP_COMMODITY','CROP_COMMODITY','Crop Commodity','FALSE'),
('CROP_SEASON','CROP_SEASON','Crop Season','FALSE'),
('FERTILIZER_TYPE','FERTILIZER_TYPE','Fertilizer Type','FALSE')
ON CONFLICT (attribute_id) DO NOTHING;
