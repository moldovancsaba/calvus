
-- Clean all triangle activities and world settings for a fresh start

TRUNCATE TABLE public.triangle_activities RESTART IDENTITY CASCADE;
TRUNCATE TABLE public.world_settings RESTART IDENTITY CASCADE;

-- Note: To delete all users, go to the Supabase dashboard:
-- Authentication > Users > (select all) > Delete

