# Sprint 13 — Next.js: Setup + Auth

**Pré-requisito:** Sprint 10 (API respondendo)

## Objetivo

Criar projeto Next.js 15 com TypeScript, configurar Supabase client, auth flow (login/logout), e estrutura de rotas protegidas.

## Stack

Next.js 15 · TypeScript · Tailwind CSS · shadcn/ui · `@supabase/ssr` · Supabase Realtime

## Tasks

| Task | Descrição | Tag | Status | Estimativa |
|---|---|---|---|---|
| T1 | `npx create-next-app@latest frontend/web` com TypeScript + Tailwind + App Router | `frontend` | ⏳ | ~10 min |
| T2 | Instalar shadcn/ui, configurar tema (dark, cores Stocky) | `frontend` | ⏳ | ~20 min |
| T3 | `@supabase/ssr` setup: `lib/supabase/server.ts` + `lib/supabase/client.ts` + middleware de sessão | `frontend` | ⏳ | ~25 min |
| T4 | Página `/login`: form email/senha → `supabase.auth.signInWithPassword` → redirect `/dashboard` | `frontend` | ⏳ | ~20 min |
| T5 | Layout protegido `app/(protected)/layout.tsx`: verifica sessão, redirect `/login` se não autenticado | `frontend` | ⏳ | ~15 min |
| T6 | Sidebar component com 7 links de navegação (Material Icons via `lucide-react`) | `frontend` | ⏳ | ~25 min |

## Contrato de saída

- `npm run dev` sobe Next.js local sem erros
- Login com credencial Supabase válida redireciona para `/dashboard`
- Sidebar renderiza os 7 links; rotas sem sessão redirecionam para `/login`

## Próximo sprint
[[phase_6/sprint_14_nextjs_pages]]
