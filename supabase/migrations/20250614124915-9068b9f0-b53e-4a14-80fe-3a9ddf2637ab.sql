
-- 1. Clear existing triangle activity data as historical data loss is accepted
TRUNCATE TABLE public.triangle_activities RESTART IDENTITY;

-- 2. Add columns for improved triangle state persistence: click_count, subdivided, and action_type
ALTER TABLE public.triangle_activities
  ADD COLUMN IF NOT EXISTS click_count integer,
  ADD COLUMN IF NOT EXISTS subdivided boolean DEFAULT false,
  ADD COLUMN IF NOT EXISTS action_type text;

-- 3. (Optional) Remove obsolete rows/columns, but KEEP old columns if used in frontend code for now for backward compatibility

-- 4. Add notes column for debug/future extensibility
ALTER TABLE public.triangle_activities
  ADD COLUMN IF NOT EXISTS notes text;

-- 5. Ensure new columns are nullable until code upgrade is done
