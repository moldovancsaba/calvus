
import React from "react";

// SVG path data sourced from public domain world blank map.
// This is a very simplified outline, not for precision use.
const WorldBlindMapSVG = () => (
  <div className="flex flex-col items-center justify-center w-full h-full">
    <svg
      viewBox="0 0 800 400"
      width="90%"
      height="90%"
      className="max-w-[95vw] max-h-[80vh]"
      style={{ background: "#f8fafc" }}
      aria-label="Simplified World Map"
    >
      <g fill="#cbd5e1" stroke="#334155" strokeWidth={1}>
        {/* Africa */}
        <path d="M448,240 l15,12 3,27 -9,36 -19,16 -15,-11 -17,-21 -2,-42 21,-16 23,-1z" />
        {/* Europe */}
        <path d="M465,145 l20,5 5,12 -19,13 -19,-2 -8,-11 21,-17z" />
        {/* North America */}
        <path d="M178,88 l84,5 32,36 -28,26 -19,38 -14,48 -30,33 -27,-15 -17,-42 1,-41 18,-34z" />
        {/* South America */}
        <path d="M265,269 l32,36 17,36 -9,43 -28,7 -33,-26 -13,-33 14,-27 20,-36z" />
        {/* Asia */}
        <path d="M490,115 l52,-13 41,8 44,31 6,19 -41,22 -51,25 -44,10 -24,-30 9,-41z" />
        {/* Australia */}
        <path d="M690,347 l30,15 8,22 -21,16 -25,-11 -3,-20 11,-22z" />
        {/* Antarctica */}
        <path d="M100,380 l200,10 130,-8 140,7 165,-5 55,12 -35,4 -290,8 -260,-10 -70,-8z" />
      </g>
      {/* Optionally: add some thin meridian/parallel lines for ambiance */}
      <g stroke="#e5e7eb" strokeWidth={0.5}>
        <line x1="0" y1="200" x2="800" y2="200" />
        <line x1="400" y1="0" x2="400" y2="400" />
      </g>
    </svg>
    <div className="mt-4 text-sm text-gray-500">Simple World Outline (Blind Map)</div>
  </div>
);

export default WorldBlindMapSVG;
