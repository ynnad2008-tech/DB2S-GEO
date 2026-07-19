-- DB2S-GEO Preview 0.1.0 — schema mínimo Supabase (PostgreSQL)
-- Tablas: search_logs · feedback · events
-- Sin PII / sin IP / sin user agents
-- Ejecutar en SQL Editor de Supabase (proyecto preview)

create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- search_logs: consultas (query · timestamp · results_count)
-- ---------------------------------------------------------------------------
create table if not exists public.search_logs (
  id uuid primary key default gen_random_uuid(),
  query text not null check (char_length(query) between 1 and 500),
  ts timestamptz not null default timezone('utc', now()),
  results_count integer not null default 0 check (results_count >= 0),
  channel text not null default 'recommend'
    check (channel in ('recommend', 'decision_support', 'explore', 'other'))
);

create index if not exists search_logs_ts_idx on public.search_logs (ts desc);
create index if not exists search_logs_query_idx on public.search_logs (query);

comment on table public.search_logs is
  'Telemetría mínima de consultas — DB2S-GEO preview';

-- ---------------------------------------------------------------------------
-- feedback: reacciones simples de colegas (preview)
-- ---------------------------------------------------------------------------
create table if not exists public.feedback (
  id uuid primary key default gen_random_uuid(),
  ts timestamptz not null default timezone('utc', now()),
  query text,
  resource_id text,
  rating smallint check (rating in (-1, 0, 1)),
  note text check (note is null or char_length(note) <= 500)
);

create index if not exists feedback_ts_idx on public.feedback (ts desc);

comment on table public.feedback is
  'Feedback mínimo de preview (útil / no útil) — sin identidad de usuario';

-- ---------------------------------------------------------------------------
-- events: clics y eventos genéricos (p. ej. resource_click)
-- ---------------------------------------------------------------------------
create table if not exists public.events (
  id uuid primary key default gen_random_uuid(),
  ts timestamptz not null default timezone('utc', now()),
  event_type text not null
    check (event_type in ('resource_click', 'orient_submit', 'other')),
  resource_id text,
  source_id text,
  query text,
  meta jsonb not null default '{}'::jsonb
);

create index if not exists events_ts_idx on public.events (ts desc);
create index if not exists events_type_idx on public.events (event_type);

comment on table public.events is
  'Eventos de interacción (clics de recurso) — DB2S-GEO preview';

-- RLS: preview interna — deshabilitar acceso anónimo por defecto
alter table public.search_logs enable row level security;
alter table public.feedback enable row level security;
alter table public.events enable row level security;

-- Políticas: solo service_role (backend). No policies para anon/authenticated.
-- Inserts desde la API con SUPABASE_SERVICE_KEY cuando se cablee.
