
/**
 * Helper utilities for useTriangleMeshTap.
 */

// Simple click streak in-memory store.
export const userTriangleClickStreak: Record<string, { triangleId: string, streak: number }> = {};

/**
 * Determines robust emoji for triangle winner.
 */
export function resolveWinnerEmoji(
  identity?: { emoji?: string },
  triangleEl?: { emoji?: string }
) {
  if (identity?.emoji && identity.emoji.trim()) return identity.emoji;
  if (triangleEl?.emoji && triangleEl.emoji.trim()) return triangleEl.emoji;
  return "🌟";
}
