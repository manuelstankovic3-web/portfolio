# Supabase postavljanje (tvojih ~5 minuta)

Ovo je jedini dio koji ja ne mogu umjesto tebe — treba tvoj račun. Nakon ovoga mi pošalji 2 vrijednosti i spajam pravi login + bazu.

## 1. Napravi projekt
1. Idi na **supabase.com** → **Start your project** → prijava (GitHub ili email).
2. **New project**. Ime: `freshfront`. Odaberi regiju **Frankfurt (EU)**. Zapamti lozinku baze.
3. Pričekaj ~1 min da se projekt kreira.

## 2. Pokreni shemu baze
1. Lijevo → **SQL Editor** → **New query**.
2. Otvori file `app/supabase-schema.sql` iz ovog repozitorija, kopiraj **sve** i zalijepi.
3. Klikni **Run**. Treba pisati "Success".

## 3. Napravi svoj admin račun
1. Lijevo → **Authentication** → **Users** → **Add user** → upiši svoj email + lozinku.
2. Klikni na tog korisnika i kopiraj njegov **User UID**.
3. Natrag u **SQL Editor**, pokreni (zamijeni UUID):
   ```sql
   insert into profiles (id, role) values ('TVOJ-UUID', 'admin');
   ```

## 4. Pošalji mi 2 vrijednosti
Lijevo → **Project Settings** → **API**. Pošalji mi:
- **Project URL** (npr. `https://xxxx.supabase.co`)
- **anon public** ključ

> Ovaj "anon" ključ je javan i siguran za web stranicu — prava zaštita podataka je u pravilima (RLS) koja smo već postavili u shemi.

Kad to pošalješ, upišem ih u `app/config.js`, spojim login i bazu, i zajedno testiramo uživo.
