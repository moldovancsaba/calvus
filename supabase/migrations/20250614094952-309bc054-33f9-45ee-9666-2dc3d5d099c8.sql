
-- 1. Create triangle_activities table in Supabase Postgres
CREATE TABLE public.triangle_activities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "when" timestamptz NOT NULL,
  "where" text NOT NULL,
  "what" integer NOT NULL,
  level integer NOT NULL,
  timestamp timestamptz NOT NULL DEFAULT now()
);

-- 2. You probably want everyone to read/write for now, disable RLS for public use:
ALTER TABLE public.triangle_activities DISABLE ROW LEVEL SECURITY;

-- 3. (Later: You can enable RLS and set up policies for auth if needed.)
