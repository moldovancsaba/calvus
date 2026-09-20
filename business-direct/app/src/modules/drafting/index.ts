import type { Listing } from '../catalogue/index.js';

/** The banned-pattern list (R32, R36): no false urgency or scarcity, no confirmshaming, no pressure on a stated vulnerability. */
const BANNED: [RegExp, string][] = [
  [/\b(today only|last chance|only \d+ (spots?|places?) left|hurry|don'?t miss out)\b/i, 'false urgency or scarcity'],
  [/\b(are you sure you want to miss|no thanks, i (don'?t|do not) want)\b/i, 'confirmshaming'],
  [/\b(limited time|ends (tonight|soon))\b/i, 'false urgency'],
  [/\b(discount|% off|percent off|coupon)\b/i, 'a discount (R13, R37)'],
];
export type Violation = { pattern: string };
export function patternGuard(text: string): Violation[] {
  const v = BANNED.filter(([re]) => re.test(text)).map(([, pattern]) => ({ pattern }));
  if (/\b(bereave|can'?t afford|please stop)\b/i.test(text)) v.push({ pattern: 'pressure on a stated vulnerability' });
  if (/\[link\]/.test(text)) v.push({ pattern: 'unresolved link' });
  return v;
}

export type DraftKind = 'sequence' | 'retain' | 'answer';
export type Draft = { copy: string; why: string; ai: false };
const first = (p: Listing) => (p.email || 'there').split('@')[0].split(/[._-]/)[0].replace(/^\w/, c => c.toUpperCase());
const merge = (tpl: string, vars: Record<string, string>) => tpl.replace(/\{(\w+)\}/g, (_, k) => vars[k] ?? `{${k}}`);

/** The drafter with the AI switch off: the listing's own text and a template with merge fields (R10). Every template carries the footer (R2, R23). */
export const templateDrafter = {
  sequence(step: 1 | 2 | 3, p: Listing, vars: { link: string; postal_address: string }): Draft {
    const tpl = {
      1: 'Hi {first} — {name} is listed on the site families in {area} use; your page is yours to manage, free. Sessions, the trial policy and photos go on it in minutes: {link}',
      2: 'Hi {first} — a family in {area} saved {name} this week. Claim your page and they hear from you first: {link}',
      3: 'Hi {first} — last note from us: {name}\'s page is waiting. One click claims it: {link}',
    }[step];
    return { copy: merge(tpl, { first: first(p), name: p.name, area: p.neighborhood || p.borough || 'your area', link: vars.link }) + `\n\n${vars.postal_address} · unsubscribe`, why: `step ${step} of the invitation`, ai: false };
  },
  retain(signal: 'renewal' | 'stale' | 'unanswered' | 'no_saves', p: Listing, numbers: { saves: number; enquiries: number; enrolled: number }, vars: { link: string; postal_address: string }): Draft {
    const tpl = {
      renewal: 'Hi {first} — your placement for {name} renews soon. Since it started: {saves} families saved you, {enquiries} asked about a trial, {enrolled} enrolled after one. Keep it as it is, or reply "call" and we go through the numbers together. {link}',
      stale: 'Hi {first} — {name}\'s page has had no session or trial update for a month, and families searching {activity} in {area} see the pages that are current first. Two minutes fixes it: {link}',
      unanswered: 'Hi {first} — a family wrote to {name} two days ago and is still waiting. Their message is in your inbox: {link}',
      no_saves: 'Hi {first} — {name} had no new saves this month. A photo and this week\'s session usually bring them back: {link}',
    }[signal];
    return { copy: merge(tpl, { first: first(p), name: p.name, area: p.neighborhood || p.borough || 'your area', activity: p.primaryActivityType || 'your activity', link: vars.link, ...Object.fromEntries(Object.entries(numbers).map(([k, v]) => [k, String(v)])) }) + `\n\n${vars.postal_address} · unsubscribe`, why: `retention: ${signal}`, ai: false };
  },
};
