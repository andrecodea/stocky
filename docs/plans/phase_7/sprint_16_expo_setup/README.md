# Sprint 16 — React Native: Setup + Auth (Expo)

**Pré-requisito:** Sprint 10 (API no ar)

## Objetivo

Criar projeto Expo com TypeScript, configurar Supabase client, auth flow, e estrutura de navegação (bottom tabs + stack).

## Stack

Expo SDK 52 · TypeScript · NativeWind (Tailwind para RN) · `@supabase/supabase-js` · Expo Router · EAS Build

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | `npx create-expo-app@latest mobile --template blank-typescript` | ⏳ | ~10 min |
| T2 | Instalar NativeWind, configurar `babel.config.js` e `tailwind.config.js` | ⏳ | ~20 min |
| T3 | `@supabase/supabase-js` + `AsyncStorage` para persistência de sessão | ⏳ | ~20 min |
| T4 | Expo Router: estrutura `app/(auth)/login.tsx` + `app/(tabs)/` | ⏳ | ~25 min |
| T5 | Tela login: email/senha → `supabase.auth.signInWithPassword` → redirect para tabs | ⏳ | ~20 min |
| T6 | Bottom tab navigator: 4 tabs com ícones Material (Home · Estoque · Movimentações · Alertas) | ⏳ | ~20 min |

## Contrato de saída

- `npx expo start` sobe sem erros
- Login com credencial Supabase válida mostra 4 tabs
- Tab inativo redireciona para login

## Próximo sprint
[[phase_7/sprint_17_mobile_tabs]]
