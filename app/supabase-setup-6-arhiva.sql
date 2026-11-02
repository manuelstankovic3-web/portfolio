-- ============================================================
-- Fresh Front — ARHIVA DOKUMENATA (pokreni JEDNOM)
-- Supabase > SQL Editor > New query > zalijepi sve > Run
-- ============================================================

-- 1) Storage bucket za dokumente (privatni)
insert into storage.buckets (id, name, public)
values ('dokumenti','dokumenti', false)
on conflict (id) do nothing;

-- 2) Tablica dokumenata (metapodaci; sama datoteka je u Storageu)
create table if not exists documents (
  id          uuid primary key default gen_random_uuid(),
  office_id   uuid references offices(id) on delete cascade,
  client_id   uuid references clients(id) on delete set null,
  client_name text,
  path        text not null,
  doc_day     date default ((now() at time zone 'Europe/Zagreb')::date),
  created_at  timestamptz default now()
);
alter table documents enable row level security;

create policy "documents office all" on documents
  for all using (office_id = my_office()) with check (office_id = my_office());
create policy "documents admin all" on documents
  for all using (is_admin()) with check (is_admin());

create index if not exists documents_idx on documents(office_id, client_id, doc_day);

-- 3) Storage pravila (mapa = office_id, pa ured vidi samo svoje)
create policy "dok read own" on storage.objects for select to authenticated
  using (bucket_id='dokumenti'
    and (storage.foldername(name))[1] = (select office_id::text from profiles where id = auth.uid()));
create policy "dok read admin" on storage.objects for select to authenticated
  using (bucket_id='dokumenti'
    and exists(select 1 from profiles where id = auth.uid() and role='admin'));
create policy "dok write own" on storage.objects for insert to authenticated
  with check (bucket_id='dokumenti'
    and (storage.foldername(name))[1] = (select office_id::text from profiles where id = auth.uid()));
create policy "dok delete own" on storage.objects for delete to authenticated
  using (bucket_id='dokumenti'
    and (storage.foldername(name))[1] = (select office_id::text from profiles where id = auth.uid()));
