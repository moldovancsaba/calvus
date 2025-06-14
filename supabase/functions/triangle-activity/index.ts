
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { MongoClient } from "https://deno.land/x/mongo@v0.32.0/mod.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  let client: MongoClient | null = null;
  try {
    const MONGODB_URI = Deno.env.get('MONGODB_URI')
    if (!MONGODB_URI) {
      throw new Error('MongoDB URI not configured')
    }

    client = new MongoClient()
    await client.connect(MONGODB_URI)
    
    const db = client.database("triangle_mesh")
    const collection = db.collection("triangle_activities")

    if (req.method === 'POST') {
      const { action, triangleId, clickCount, level } = await req.json()
      
      if (action === 'clear') {
        // Clear all data from the collection
        await collection.deleteMany({})
        console.log('All triangle activities cleared from MongoDB')
        await client.close()
        return new Response(
          JSON.stringify({ success: true, message: 'Database cleared' }),
          { 
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            status: 200 
          }
        )
      }

      if (action === 'click') {
        // Store triangle click activity
        const activity = {
          when: new Date().toISOString(),
          where: triangleId,
          what: clickCount,
          level: level,
          timestamp: new Date()
        }

        const result = await collection.insertOne(activity)
        console.log(`Stored triangle activity: ${JSON.stringify(activity)}`)
        await client.close()
        return new Response(
          JSON.stringify({ success: true, activityId: result.insertedId }),
          { 
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            status: 200 
          }
        )
      }
    }

    if (req.method === 'GET') {
      // Retrieve all activities
      let activities = [];
      try {
        activities = await collection.find({}).toArray();
      } catch (err) {
        // Defensive: return empty array (not null, not undefined)
        console.error("Mongo find error:", err);
        activities = [];
      }

      // Defensive: always return as array
      if (!Array.isArray(activities)) activities = [];
      
      await client.close();
      return new Response(
        JSON.stringify({ activities }),
        { 
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          status: 200 
        }
      )
    }

    await client.close()
    return new Response(
      JSON.stringify({ error: 'Method not allowed' }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 405 
      }
    )

  } catch (error) {
    console.error('MongoDB operation failed:', error)
    if (client) {
      try { await client.close(); } catch {}
    }
    // Always return a valid JSON object, never plain text
    return new Response(
      JSON.stringify({ error: error instanceof Error ? error.message : 'Unknown error' }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500 
      }
    )
  }
})
