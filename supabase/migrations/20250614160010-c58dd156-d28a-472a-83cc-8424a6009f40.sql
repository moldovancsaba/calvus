
-- Enable Row Level Security (RLS) on world_settings
ALTER TABLE public.world_settings ENABLE ROW LEVEL SECURITY;

-- Add a policy allowing anyone to select (read) world settings
CREATE POLICY "Allow read to anyone"
  ON public.world_settings
  FOR SELECT
  USING (true);

-- Add a policy allowing anyone to update world settings
CREATE POLICY "Allow update to anyone"
  ON public.world_settings
  FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- Add a policy allowing anyone to insert world settings (for new worlds)
CREATE POLICY "Allow insert to anyone"
  ON public.world_settings
  FOR INSERT
  WITH CHECK (true);
