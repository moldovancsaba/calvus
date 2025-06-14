
import React from "react";

export function LoadingOverlay() {
  return (
    <div className="absolute inset-0 flex items-center justify-center bg-white/90 backdrop-blur-[2px] z-50 rounded-none p-4">
      <div className="text-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
        <p className="text-base text-gray-600">Loading...</p>
      </div>
    </div>
  );
}
