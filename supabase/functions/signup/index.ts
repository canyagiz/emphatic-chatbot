import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { withCorsHeaders } from "../utils/withCorsHeaders.ts";
import { supabaseClientInit } from "../utils/clientInitializatior.ts";


serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      status: 200,
      headers: withCorsHeaders(),
    });
  }

  let email = "";
  let password = "";

  try {
    const body = await req.json();
    email = body.email;
    password = body.password;
  } catch (err) {
    return new Response(JSON.stringify({ error: "Geçersiz JSON body" }), {
      status: 400,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });
  }

  if (!email || !password) {
    return new Response(JSON.stringify({ error: "Email ve şifre gerekli" }), {
      status: 400,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });
  }

  const supabase = supabaseClientInit();

  const { data, error } = await supabase.auth.signUp({ email, password });

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: withCorsHeaders({ "Content-Type": "application/json" }),
    });
  }

  return new Response(JSON.stringify(data), {
    status: 201,
    headers: withCorsHeaders({ "Content-Type": "application/json" }),
  });
});
