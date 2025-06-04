import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.4";
import { withCorsHeaders } from "../utils/withCorsHeaders.ts";


serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      status: 200,
      headers: withCorsHeaders(),
    });
  }
  
  const { email, password } = await req.json();

  if (!email || !password) {
    return new Response(JSON.stringify({ error: "Email and password required" }), {
      status: 400,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });
  }

  const supabase = createClient(
    Deno.env.get("PUBLIC_URL")!,
    Deno.env.get("PUBLIC_ANON_KEY")!
  );

  const { data, error } = await supabase.auth.signInWithPassword({ email, password });

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 401,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });
  }

  return new Response(JSON.stringify(data), {
    status: 200,
    headers: withCorsHeaders({ "Content-Type": "application/json" }),
  });
});
