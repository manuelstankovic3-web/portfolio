-- ============================================================
-- Fresh Front — JEDNOKRATNI setup (pokreni samo JEDNOM)
-- Nakon ovoga sve dodaješ kroz stranicu, bez SQL-a.
-- Supabase > SQL Editor > New query > zalijepi sve > Run
-- ============================================================

-- Automatski napravi profil za svaki novi ured (iz podataka pri registraciji)
create or replace function handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, role, office_id)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'role', 'office'),
    nullif(new.raw_user_meta_data->>'office_id','')::uuid
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function handle_new_user();
