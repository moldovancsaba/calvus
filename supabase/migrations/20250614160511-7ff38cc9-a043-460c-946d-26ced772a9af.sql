
-- Enable RLS on triangle_activities if not already done (no effect if already enabled)
ALTER TABLE public.triangle_activities ENABLE ROW LEVEL SECURITY;

-- Allow anyone to SELECT (read)
CREATE POLICY "Allow read to anyone"
  ON public.triangle_activities
  FOR SELECT
  USING (true);

-- Allow anyone to INSERT (write activity)
CREATE POLICY "Allow insert to anyone"
  ON public.triangle_activities
  FOR INSERT
  WITH CHECK (true);

-- Allow anyone to UPDATE activity (optional, safe mirror)
CREATE POLICY "Allow update to anyone"
  ON public.triangle_activities
  FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- Allow anyone to DELETE activity (optional, safe mirror)
CREATE POLICY "Allow delete to anyone"
  ON public.triangle_activities
  FOR DELETE
  USING (true);
