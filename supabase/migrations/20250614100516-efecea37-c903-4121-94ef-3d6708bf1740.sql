
-- Enable Row Level Security on the triangle_activities table
ALTER TABLE public.triangle_activities ENABLE ROW LEVEL SECURITY;

-- Create a policy so any user (even unauthenticated) can select data
CREATE POLICY "Public read access" ON public.triangle_activities
  FOR SELECT USING (true);

-- Create a policy so any user (even unauthenticated) can insert data
CREATE POLICY "Public insert access" ON public.triangle_activities
  FOR INSERT WITH CHECK (true);

-- Create a policy so any user (even unauthenticated) can update data
CREATE POLICY "Public update access" ON public.triangle_activities
  FOR UPDATE USING (true);

-- Create a policy so any user (even unauthenticated) can delete data
CREATE POLICY "Public delete access" ON public.triangle_activities
  FOR DELETE USING (true);
