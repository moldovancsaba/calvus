
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";

const Index = () => {
  const [slug, setSlug] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleJoin = (e: React.FormEvent) => {
    e.preventDefault();
    // Allow blank for original world
    const world = slug.trim();
    if (world === "") {
      navigate("/game");
    } else if (!/^[A-Za-z0-9_-]{1,32}$/.test(world)) {
      setError("Game slug must be 1-32 characters and contain only letters, numbers, underscore, or dash.");
    } else {
      navigate(`/game/${world}`);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-100 to-white">
      <form
        onSubmit={handleJoin}
        className="bg-white/95 rounded-xl shadow-2xl p-6 flex flex-col items-center gap-6 border"
        style={{ minWidth: 320, maxWidth: 380 }}
      >
        <h1 className="text-2xl font-bold text-center mb-1">Join or Create a World</h1>
        <input
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-center text-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
          placeholder="Enter world slug (e.g. GAMER16WORLD) or leave blank"
          maxLength={32}
          value={slug}
          onChange={(e) => setSlug(e.target.value.replace(/[^A-Za-z0-9_-]/g, ""))}
        />
        <Button className="w-full py-3 text-lg" type="submit">Enter World</Button>
        <div className="text-xs text-muted-foreground text-center">
          <p className="mb-1">If the slug exists, you will join that world. Otherwise, a new world is created!</p>
          <p>Leave blank to join the original (global) world.</p>
        </div>
        {error && <div className="text-sm text-red-500 text-center">{error}</div>}
      </form>
    </div>
  );
};

export default Index;
