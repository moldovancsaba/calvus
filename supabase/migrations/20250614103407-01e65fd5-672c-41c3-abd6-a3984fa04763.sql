
-- Add columns for gametag and color to persist identity with every triangle action

ALTER TABLE public.triangle_activities
  ADD COLUMN gametag text,
  ADD COLUMN color text;

-- (Keeps both columns nullable for backward compatibility)

