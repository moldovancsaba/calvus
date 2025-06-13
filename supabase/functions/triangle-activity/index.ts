
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

  try {
    const MONGODB_URI = Deno.env.get('MONGODB_URI')
    if (!MONGODB_URI) {
      throw new Error('MongoDB URI not configured')
    }

    const client = new MongoClient()
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
          when: new Date().toISOString(), // UTC ISO 8601 with milliseconds
          where: triangleId, // hierarchical triangle ID (e.g., "1.4.2")
          what: clickCount, // level of clicks on this triangle
          level: level, // subdivision level
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
      const activities = await collection.find({}).toArray()
      
      await client.close()
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
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500 
      }
    )
  }
})
