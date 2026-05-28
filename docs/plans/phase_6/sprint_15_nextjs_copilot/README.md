# Sprint 15 — Next.js: Copilot FAB

**Pré-requisito:** Sprint 14 (páginas) + Sprint 12 (RAG pipeline)

## Objetivo

Widget de chat flutuante (FAB bottom-right) acessível em todas as páginas. Conecta ao `POST /v1/ai/chat` SSE e renderiza respostas em streaming.

## Tasks

| Task | Descrição | Tag | Status | Estimativa |
|---|---|---|---|---|
| T1 | `components/Copilot/CopilotFab.tsx`: botão flutuante que abre/fecha o painel de chat | `frontend` | ⏳ | ~20 min |
| T2 | `components/Copilot/CopilotPanel.tsx`: painel de chat com histórico de mensagens, input, indicador de digitação | `frontend` | ⏳ | ~35 min |
| T3 | `lib/copilot.ts`: função `streamChat(message)` que consome SSE de `POST /v1/ai/chat` e retorna AsyncGenerator de deltas | `frontend` | ⏳ | ~25 min |
| T4 | Integrar `CopilotFab` no layout protegido `app/(protected)/layout.tsx` | `frontend` | ⏳ | ~10 min |
| T5 | Testar end-to-end: pergunta → SSE stream → tokens renderizando em tempo real | `frontend` | ⏳ | ~15 min |

## Contrato de saída

- FAB visível em todas as páginas do admin
- Chat abre sem recarregar página
- Resposta aparece token por token
- Histórico da sessão persiste enquanto a aba está aberta

## Referência visual

`docs/architecture/nextjs-screens.html` (Copilot widget no canto inferior direito)
