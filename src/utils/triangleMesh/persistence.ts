
import type { TriangleMesh } from "./geometry";

// TypeScript type for DB row with new columns
type TriangleActivityRow = {
  id: string;
  when: string;
  where: string;
  what?: string | number | null; // Now can be string action_type
  click_count?: number | null;
  level: number;
  subdivided?: boolean | null;
  timestamp: string;
  gametag?: string | null;
  color?: string | null;
  notes?: string | null;
  action_type?: string | null;
};

// Store full triangle state on every write
export async function storeTriangleActivity(
  triangleId: string,
  clickCount: number,
  level: number,
  subdivided: boolean,
  action_type: string,
  gametag?: string,
  color?: string,
  notes?: string
) {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { error, data } = await supabase
      .from('triangle_activities')
      .insert([
        {
          when: new Date().toISOString(),
          where: triangleId,
          what: action_type,
          click_count: clickCount,
          level: level,
          subdivided: subdivided,
          gametag: gametag ?? null,
          color: color ?? null,
          notes: notes ?? null,
          action_type: action_type,
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

// Clear all triangle activities
export async function clearTriangleActivities() {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { error } = await supabase
      .from('triangle_activities')
      .delete();
    if (error) throw error;
    return { success: true };
  } catch (error) {
    console.error('Error clearing triangle activities in Supabase:', error);
    throw error;
  }
}

// Get all triangle activities from Supabase
// Each row is now a full triangle state
export async function getTriangleActivities() {
  try {
    const { supabase } = await import('@/integrations/supabase/client');
    const { data, error } = await supabase
      .from('triangle_activities')
      .select('*');
    if (error) throw error;
    if (!Array.isArray(data)) return [];
    const activities: TriangleActivityRow[] = data.map((act) => ({
      ...act,
      when: typeof act.when === 'string' ? act.when : new Date(act.when).toISOString(),
      subdivided: act.subdivided ?? false,
      gametag: act.gametag ?? null,
      color: act.color ?? null,
      notes: act.notes ?? null,
      action_type: act.action_type ?? (typeof act.what === 'string' ? act.what : null),
    }));
    return activities;
  } catch (error) {
    console.error('Error getting triangle activities from Supabase:', error);
    return [];
  }
}
