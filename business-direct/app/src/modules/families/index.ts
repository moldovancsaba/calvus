import type { FamilyPrefs, OutboxRow } from '../../db/schemas.js';
import type { Store } from '../../lib/store.js';
import type { EventLog } from '../../lib/events.js';
import { cancelFor } from '../outbox/index.js';

type F = FamilyPrefs & { _id: string };
/** Stop turns every channel off (or one) and cancels what is queued — one operation (ADR-6, R28). */
export async function stop(familyId: string, platformId: string, families: Store<F>, outbox: Store<OutboxRow>, consents: Store<{ _id: string; family_id: string; channel: string; revoked_at: number | null; text: string }>, events: EventLog, channel?: OutboxRow['channel']) {
  const f = (await families.find(x => x.family_id === familyId && x.platform_id === platformId))[0]; if (!f) return;
  const prefs = channel ? { ...f.prefs, [({ email: 'picks', push: 'alerts', sms: 'sms' } as any)[channel]]: false } : { picks: false, alerts: false, nearby: false, sms: false };
  await families.update(f._id, { prefs, stopped_at: channel ? f.stopped_at : new Date().toISOString(), version: f.version + 1 }, { version: f.version });
  await consents.put({ _id: `stop-${familyId}-${Date.now()}`, family_id: familyId, channel: channel ?? 'all', revoked_at: Date.now(), text: 'STOP' });
  await cancelFor(familyId, outbox, channel);
  await events.emit(platformId, 'family.stopped', { family_id: familyId, channel });
}
