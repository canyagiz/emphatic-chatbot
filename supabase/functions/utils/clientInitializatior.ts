import { SupabaseClient, createClient } from "https://esm.sh/@supabase/supabase-js@2";

export function supabaseClientInit(): SupabaseClient  {
    const supabase = createClient(
        Deno.env.get("PUBLIC_URL")!,
        Deno.env.get("PUBLIC_ANON_KEY")!
      );
      return supabase;
}