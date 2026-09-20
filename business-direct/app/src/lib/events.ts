/** The append-only event log (ADR-11). In production a MongoDB collection; here an array. */
export type Event = { platform_id: string; at: number; name: string; props: Record<string, unknown> };
export class EventLog {
  readonly rows: Event[] = [];
  async emit(platform_id: string, name: string, props: Record<string, unknown> = {}) { this.rows.push({ platform_id, at: Date.now(), name, props }); }
  count(name: string) { return this.rows.filter(e => e.name === name).length; }
}
