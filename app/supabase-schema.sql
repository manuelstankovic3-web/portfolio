-- ============================================================
-- Fresh Front — shema baze za Supabase
-- Zalijepite CIJELI ovaj file u Supabase > SQL Editor > New query > Run
-- ============================================================

-- 1) PROFILES — povezuje prijavljenog korisnika s ulogom i uredom
create table if not exists profiles (
  id        uuid primary key references auth.users(id) on delete cascade,
  role      text not null default 'office' check (role in ('admin','office')),
  office_id uuid
);

-- 2) OFFICES — vaši pretplatnici (uredi)
create table if not exists offices (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  login_email text,
  price       numeric default 0,
  status      text not null default 'trial' check (status in ('trial','paid','unpaid')),
  due_date    date,
  created_at  timestamptz default now()
);

-- 3) CLIENTS — klijenti (firme) pojedinog ureda
create table if not exists clients (
  id           uuid primary key default gen_random_uuid(),
  office_id    uuid not null references offices(id) on delete cascade,
  name         text not null,
  email        text,
  phone        text,
  items        jsonb default '[]'::jsonb,   -- checklist dokumenata
  request_sent boolean default false,
  created_at   timestamptz default now()
);

-- ---- pomoćne funkcije ----
create or replace function is_admin() returns boolean
  language sql security definer stable as $$
  select exists(select 1 from profiles where id = auth.uid() and role = 'admin');
$$;

create or replace function my_office() returns uuid
  language sql security definer stable as $$
  select office_id from profiles where id = auth.uid();
$$;

-- ---- uključi sigurnost na razini retka ----
alter table profiles enable row level security;
alter table offices  enable row level security;
alter table clients  enable row level security;

-- PROFILES: svatko vidi svoj profil; admin vidi sve
create policy "profiles read" on profiles
  for select using (id = auth.uid() or is_admin());

-- OFFICES: admin radi sve; ured vidi samo svoj
create policy "offices admin all" on offices
  for all using (is_admin()) with check (is_admin());
create policy "offices own read" on offices
  for select using (id = my_office());

-- CLIENTS: admin sve; ured upravlja SAMO svojim klijentima
create policy "clients admin all" on clients
  for all using (is_admin()) with check (is_admin());
create policy "clients office own" on clients
  for all using (office_id = my_office()) with check (office_id = my_office());

-- ============================================================
-- NAKON POKRETANJA GORNJEG:
--
-- A) Napravite SVOJ admin račun:
--    Authentication > Users > Add user  (vaš email + lozinka)
--    Zatim kopirajte UUID tog korisnika i pokrenite:
--      insert into profiles (id, role) values ('VAS-UUID-OVDJE', 'admin');
--
-- B) Za svaki NOVI ured (pretplatnika):
--    1. Authentication > Users > Add user  (email ureda + lozinka)  -> kopirajte UUID
--    2. U admin konzoli dodate ured (dobijete OFFICE-ID), ili ovdje:
--         insert into offices (name, login_email, price, status)
--         values ('Naziv ureda', 'ured@mail.hr', 49, 'trial')
--         returning id;
--    3. Povežite korisnika i ured:
--         insert into profiles (id, role, office_id)
--         values ('UUID-UREDA', 'office', 'OFFICE-ID-IZ-KORAKA-2');
-- ============================================================
