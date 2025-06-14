
import type { TriangleMesh } from "./geometry";

// TypeScript type for DB row
type TriangleActivityRow = {
  id: string;
  when: string;
  where: string;
  what: number;
  level: number;
  timestamp: string;
};

// Store triangle click activity in Supabase
export async function storeTriangleActivity(triangleId: string, clickCount: number, level: number) {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { error, data } = await supabase
      .from('triangle_activities')
      .insert([
        {
          when: new Date().toISOString(),
          where: triangleId,
          what: clickCount,
          level: level,
        }
      ])
      .select('id');
    if (error) {
      throw error;
    }
    const typedData = data as TriangleActivityRow[] | null;
    return { success: true, id: typedData?.[0]?.id };
  } catch (error) {
    console.error('Error storing triangle activity in Supabase:', error);
    throw error;
  }
}

// Clear all triangle activities from Supabase
export async function clearTriangleActivities() {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { error } = await supabase
      .from('triangle_activities')
      .delete();
    if (error) {
      throw error;
    }
    console.log('Triangle activities cleared successfully in Supabase');
    return { success: true };
  } catch (error) {
    console.error('Error clearing triangle activities in Supabase:', error);
    throw error;
  }
}

// Get all triangle activities from Supabase
export async function getTriangleActivities() {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { data, error } = await supabase
      .from('triangle_activities')
      .select('*');
    if (error) {
      throw error;
    }
    if (!Array.isArray(data)) {
      console.warn("Triangle activities GET: Malformed response or 'activities' is not array", data);
      return [];
    }
    const activities = (data as TriangleActivityRow[]).map((act) => ({
      ...act,
      when: typeof act.when === 'string' ? act.when : new Date(act.when).toISOString(),
    }));
    console.log('Retrieved triangle activities from Supabase:', activities.length, activities);
    return activities;
  } catch (error) {
    console.error('Error getting triangle activities from Supabase:', error);
    return [];
  }
}
