import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { withCorsHeaders } from "../utils/withCorsHeaders.ts";
import { supabaseClientInit } from "../utils/clientInitializatior.ts";


const supabase = supabaseClientInit();


serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("OK", {
      headers: withCorsHeaders(),
    });
  }
  
  const url = new URL(req.url);

  // Yeni oturum oluşturma
  if (url.pathname === "/sessions" && req.method === "POST") {
    try {
      const authHeader = req.headers.get("Authorization");
      if (!authHeader) {
        return new Response(JSON.stringify({ error: "No authorization header" }), { status: 401 });
      }
      const access_token = authHeader.replace("Bearer ", "");

      const { data: { user }, error } = await supabase.auth.getUser(access_token);
      if (error || !user) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
      }

      const { data, error: insertError } = await supabase
        .from("sessions")
        .insert({ user_id: user.id })
        .select("id")
        .single();

      if (insertError) {
        console.log(insertError)
        return new Response(JSON.stringify({ error: insertError.message }), { status: 500 });
      }

      return new Response(JSON.stringify({ session_id: data.id }), {
        headers: withCorsHeaders({ "Content-Type": "application/json" }),
      });
    } catch (e) {
      const error = e as Error;
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
  }
  else if (url.pathname === "/sessions" && req.method === "GET") {
    try {
      const authHeader = req.headers.get("Authorization");
      if (!authHeader) {
        return new Response(JSON.stringify({ error: "No authorization header" }), { status: 401 });
      }
      const access_token = authHeader.replace("Bearer ", "");
      const { data: { user }, error } = await supabase.auth.getUser(access_token);
      if (error || !user) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
      }
      const { data, error: selectError } = await supabase
        .from("sessions")
        .select("id")
        .eq("user_id", user.id);
      if (selectError) {
        console.log(selectError)
        return new Response(JSON.stringify({ error: selectError.message }), { status: 500 });
      }
      return new Response(JSON.stringify(data), {
        headers: withCorsHeaders({ "Content-Type": "application/json" }),      });
    } catch (e) {
      const error = e as Error;
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
  }
  else if (url.pathname === "/sessions" && req.method === "DELETE") {
    try {
      const authHeader = req.headers.get("Authorization");
      if (!authHeader) {
        return new Response(JSON.stringify({ error: "No authorization header" }), { status: 401 });
      }
      const access_token = authHeader.replace("Bearer ", "");
      const { data: { user }, error } = await supabase.auth.getUser(access_token);
      if (error || !user) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
      }
      const { session_id } = await req.json();
      
      const { data, error: deleteError } = await supabase
        .from("sessions")
        .delete()
        .eq("user_id", user.id)
        .eq("id", session_id);
      if (deleteError) {
        console.log(deleteError)
        return new Response(JSON.stringify({ error: deleteError.message }), { status: 500 });
      }
      return new Response(JSON.stringify(data), {
        headers: withCorsHeaders({ "Content-Type": "application/json" }),      });

    } catch (e) {
      const error = e as Error;
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
  }

  return new Response("Not found", { status: 404 });
});
