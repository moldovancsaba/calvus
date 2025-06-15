
import React from "react";

export function ErrorBanner({ message }: { message?: string | null }) {
  if (!message) return null;
  return (
    <div className="absolute top-2 left-1/2 -translate-x-1/2 z-50 rounded bg-yellow-100 text-yellow-900 px-4 py-2 text-xs shadow border border-yellow-300">
      {message}
    </div>
  );
}
