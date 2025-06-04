import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { withCorsHeaders } from "../utils/withCorsHeaders.ts";
import { supabaseClientInit } from "../utils/clientInitializatior.ts";

const supabase = supabaseClientInit();

serve(async (req) => {
  // ✅ CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("OK", {
      headers: withCorsHeaders(),
    });
  }
  try {
    if (req.method !== "POST") {
      return new Response(JSON.stringify({ error: "Only POST supported" }), { status: 405, headers: withCorsHeaders({ "Content-Type": "application/json" }) });
    }

    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(JSON.stringify({ error: "Missing Authorization header" }), { status: 401, headers: withCorsHeaders({ "Content-Type": "application/json" }) });
    }

    const token = authHeader.replace("Bearer ", "");
    const {
      data: { user },
      error
    } = await supabase.auth.getUser(token);

    if (error || !user) {
      return new Response(JSON.stringify({ error: "Invalid token" }), { status: 401, headers: withCorsHeaders({ "Content-Type": "application/json" }) });
    }

    const { session_id, message } = await req.json();

    const pyResponse = await fetch(Deno.env.get("PUBLIC_AI_CHAT_URL")!, {
      method: "POST",
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
      body: JSON.stringify({
        user_id: user.id,
        session_id,
        message
      })
    });

    const data = await pyResponse.json();
    return new Response(JSON.stringify(data), { status: 200, headers: withCorsHeaders({ "Content-Type": "application/json" }) });

  } catch (e) {
    console.error("Chat error:", e);
    return new Response(JSON.stringify({ error: "Internal error" }), { status: 500, headers: withCorsHeaders({ "Content-Type": "application/json" }) });
  }
});
