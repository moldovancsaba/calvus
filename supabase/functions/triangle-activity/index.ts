
// Add extra debug logging and health check endpoint.

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { MongoClient } from "https://deno.land/x/mongo@v0.32.0/mod.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  let client: MongoClient | null = null;
  try {
    const MONGODB_URI = Deno.env.get('MONGODB_URI');
    if (!MONGODB_URI) {
      console.error('Missing MONGODB_URI secret');
      return new Response(
        JSON.stringify({ error: 'MongoDB URI not configured' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
      );
    }

    // Health check endpoint: GET with ?testdb=true only attempts to connect
    const url = new URL(req.url);
    if (req.method === 'GET' && url.searchParams.get('testdb') === 'true') {
      console.log('Running MongoDB connection health check');
      client = new MongoClient();
      try {
        await client.connect(MONGODB_URI);
        await client.close();
        return new Response(
          JSON.stringify({ success: true, message: 'MongoDB connection OK' }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 }
        );
      } catch (healthErr) {
        console.error('MongoDB health check failed:', healthErr);
        if (client) try { await client.close(); } catch(e) {}
        return new Response(
          JSON.stringify({ error: 'Failed MongoDB healthcheck', details: healthErr instanceof Error ? healthErr.message : String(healthErr) }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
        );
      }
    }

    client = new MongoClient();
    console.log("Connecting to MongoDB...");
    await client.connect(MONGODB_URI);
    console.log("MongoDB connection established.");

    const db = client.database("triangle_mesh");
    const collection = db.collection("triangle_activities");

    if (req.method === 'POST') {
      let body: any;
      try {
        body = await req.json();
      } catch (jsonErr) {
        console.error('POST body parse error:', jsonErr);
        await client.close();
        return new Response(
          JSON.stringify({ error: 'Invalid JSON body' }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
        );
      }
      const { action, triangleId, clickCount, level } = body;

      if (action === 'clear') {
        try {
          const delRes = await collection.deleteMany({});
          console.log('All triangle activities cleared. Result:', delRes);
        } catch (clearErr) {
          console.error('Error clearing activities:', clearErr);
          await client.close();
          return new Response(
            JSON.stringify({ error: 'Failed to clear activities', details: clearErr instanceof Error ? clearErr.message : clearErr }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
          );
        }
        await client.close();
        return new Response(
          JSON.stringify({ success: true, message: 'Database cleared' }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 }
        );
      }

      if (action === 'click') {
        const activity = {
          when: new Date().toISOString(),
          where: triangleId,
          what: clickCount,
          level: level,
          timestamp: new Date()
        };
        let result: any = {};
        try {
          result = await collection.insertOne(activity);
          console.log(`Stored triangle activity id ${result.insertedId}:`, activity);
        } catch (insertErr) {
          console.error('Insert error:', insertErr);
          await client.close();
          return new Response(
            JSON.stringify({ error: 'Failed to insert activity', details: insertErr instanceof Error ? insertErr.message : insertErr }),
            { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
          );
        }
        await client.close();
        return new Response(
          JSON.stringify({ success: true, activityId: result.insertedId }),
          { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 }
        );
      }

      await client.close();
      return new Response(
        JSON.stringify({ error: 'Unsupported action' }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
      );
    }

    if (req.method === 'GET') {
      let activities: any[] = [];
      try {
        activities = await collection.find({}).toArray();
        console.log("Fetched activities:", activities.length);
      } catch (err) {
        console.error("Mongo find error:", err);
        activities = [];
      }
      if (!Array.isArray(activities)) activities = [];
      await client.close();
      return new Response(
        JSON.stringify({ activities }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 }
      );
    }

    // Method not allowed (still return JSON, not plain!)
    if (client) await client.close();
    return new Response(
      JSON.stringify({ error: 'Method not allowed' }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 405 }
    );
  } catch (error) {
    console.error('MongoDB operation failed:', error);
    if (client) {
      try { await client.close(); } catch(e) {console.error("Failed to close client:", e);}
    }
    // Always return JSON, never plain/HTML!
    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : String(error) }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
})
