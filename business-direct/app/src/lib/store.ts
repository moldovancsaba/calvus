/** ponytail: an in-memory store with the four calls the modules need; the Mongoose repositories
 *  implement the same interface in production. Keeps the modules testable without a database. */
export interface Store<T extends { _id: string }> {
  get(id: string): Promise<T | undefined>;
  put(doc: T): Promise<void>;
  find(pred: (d: T) => boolean): Promise<T[]>;
  update(id: string, patch: Partial<T>, expectState?: Partial<T>): Promise<T | undefined>;
}
export class MemoryStore<T extends { _id: string }> implements Store<T> {
  private m = new Map<string, T>();
  async get(id: string) { return this.m.get(id); }
  async put(doc: T) { this.m.set(doc._id, structuredClone(doc)); }
  async find(pred: (d: T) => boolean) { return [...this.m.values()].filter(pred).map(d => structuredClone(d)); }
  /** Atomic compare-and-set: the patch applies only when every field of expectState still matches. */
  async update(id: string, patch: Partial<T>, expectState?: Partial<T>) {
    const cur = this.m.get(id); if (!cur) return undefined;
    if (expectState && Object.entries(expectState).some(([k, v]) => (cur as any)[k] !== v)) return undefined;
    const next = { ...cur, ...patch }; this.m.set(id, next); return structuredClone(next);
  }
}
/** The counters and locks the cap check needs (Upstash in production; ADR-3). INCR is atomic. */
export interface Counter { incr(key: string): Promise<number>; get(key: string): Promise<number>; decr(key: string): Promise<number>; setnx(key: string): Promise<boolean>; del(key: string): Promise<void>; }
export class MemoryCounter implements Counter {
  private m = new Map<string, number>();
  async incr(k: string) { const v = (this.m.get(k) ?? 0) + 1; this.m.set(k, v); return v; }
  async get(k: string) { return this.m.get(k) ?? 0; }
  async decr(k: string) { const v = (this.m.get(k) ?? 0) - 1; this.m.set(k, v); return v; }
  async setnx(k: string) { if (this.m.has(k)) return false; this.m.set(k, 1); return true; }
  async del(k: string) { this.m.delete(k); }
}
