
import React, { useState } from "react";

const docsList = [
  { file: "README.md", label: "User Guide (README)" },
  { file: "technical-architecture.md", label: "Technical Architecture" },
  { file: "performance-optimizations.md", label: "Performance Optimizations" },
  { file: "security-scalability.md", label: "Security & Scalability" },
  { file: "CHANGELOG.md", label: "Changelog" },
];

function loadFile(filepath: string): Promise<string> {
  return fetch(`/${filepath}`)
    .then(r => r.ok ? r.text() : Promise.reject("not found"))
    .catch(() => fetch(`/src/${filepath}`).then(r => r.text()));
}

export default function DocumentsPage() {
  const [selected, setSelected] = useState(docsList[0].file);
  const [content, setContent] = useState<string>("Loading...");
  React.useEffect(() => {
    let cancelled = false;
    loadFile(selected)
      .then(text => { if (!cancelled) setContent(text); })
      .catch(() => { if (!cancelled) setContent("Could not load document."); });
    return () => { cancelled = true; };
  }, [selected]);

  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <div className="flex gap-3 mb-6 border-b pb-2 items-center">
        <div className="font-bold text-xl">Documentation</div>
        <div className="ml-auto flex gap-2">
          {docsList.map(doc =>
            <button
              key={doc.file}
              onClick={() => setSelected(doc.file)}
              className={`px-2 py-1 rounded text-sm ${selected === doc.file ? "bg-primary text-primary-foreground" : "bg-muted"}`}
            >{doc.label}</button>
          )}
        </div>
      </div>
      <div className="prose prose-sm dark:prose-invert max-w-none" style={{ whiteSpace: "pre-wrap" }}>
        {content}
      </div>
    </div>
  );
}
