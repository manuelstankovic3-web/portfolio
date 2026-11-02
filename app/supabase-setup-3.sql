-- ============================================================
-- Fresh Front — PORUKE (pokreni JEDNOM u SQL Editoru)
-- ============================================================

create table if not exists messages (
  id             uuid primary key default gen_random_uuid(),
  office_id      uuid references offices(id) on delete cascade, -- null = poruka potencijalnog klijenta (lead)
  sender         text not null check (sender in ('office','admin','lead')),
  lead_name      text,
  lead_contact   text,
  body           text not null,
  read_by_admin  boolean default false,
  created_at     timestamptz default now()
);

alter table messages enable row level security;

-- Potencijalni klijent (nije prijavljen) smije SAMO ubaciti svoju poruku
create policy "messages lead insert" on messages
  for insert to anon with check (sender = 'lead' and office_id is null);

-- Prijavljeni ured: čita i šalje svoje poruke
create policy "messages office select" on messages
  for select using (office_id = my_office());
create policy "messages office insert" on messages
  for insert with check (office_id = my_office() and sender = 'office');

-- Admin (ti): sve
create policy "messages admin all" on messages
  for all using (is_admin()) with check (is_admin());

-- Brže dohvaćanje
create index if not exists messages_office_idx on messages(office_id, created_at);
