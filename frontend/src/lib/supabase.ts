import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  // In a real app we'd throw an error, but for build process we might want to be lenient if env vars are missing
  console.warn("Supabase keys are missing")
}

export const supabase = createClient(supabaseUrl || '', supabaseAnonKey || '')
