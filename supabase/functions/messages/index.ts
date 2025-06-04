import { withCorsHeaders } from "../utils/withCorsHeaders.ts";
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
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
    // ✅ Authorization kontrolü
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) {
      return new Response(JSON.stringify({ error: "No authorization header" }), {
        status: 401,
        headers: withCorsHeaders({ "Content-Type": "application/json" }),
      });
    }

    const access_token = authHeader.replace("Bearer ", "");

    // ✅ Kullanıcıyı token'dan al
    const { data: { user }, error: userError } = await supabase.auth.getUser(access_token);
    if (userError || !user) {
      return new Response(JSON.stringify({ error: "Unauthorized" }), {
        status: 401,
        headers: withCorsHeaders({ "Content-Type": "application/json" }),
      });
    }

    // ✅ session_id sorgu parametresinden alınır
    const url = new URL(req.url);
    const sessionId = url.searchParams.get("session_id");

    if (!sessionId) {
      return new Response(JSON.stringify({ error: "Session ID is required" }), {
        status: 400,
        headers: withCorsHeaders({ "Content-Type": "application/json" }),
      });
    }

    // ✅ Chat geçmişini getir
    const { data, error: historyError } = await supabase
      .from("chat_history")
      .select("content,role") // 👈 daha anlamlı
      .eq("session_id", sessionId)
      .order("created_at", { ascending: true });

    if (historyError) {
      return new Response(JSON.stringify({ error: historyError.message }), {
        status: 500,
        headers: withCorsHeaders({ "Content-Type": "application/json" }),
      });
    }

    return new Response(JSON.stringify(data), {
      status: 200,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: "Internal Server Error", headers: withCorsHeaders({ "Content-Type": "application/json" }) }), {
      status: 500,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });
  }
});
