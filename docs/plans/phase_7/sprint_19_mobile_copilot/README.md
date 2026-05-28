# Sprint 19 — React Native: Copilot FAB

**Pré-requisito:** Sprint 17 (tabs) + Sprint 12 (RAG pipeline)

## Objetivo

FAB verde em todas as tabs abre chat full-screen com o Stocky Copilot. SSE streaming de respostas.

## Tasks

| Task | Descrição | Status | Estimativa |
|---|---|---|---|
| T1 | `components/CopilotFab.tsx`: botão verde flutuante, renderizado sobre cada tab | ⏳ | ~15 min |
| T2 | Screen `CopilotScreen`: chat full-screen com FlatList de mensagens + input + botão enviar | ⏳ | ~30 min |
| T3 | `lib/copilot.ts`: função `streamChat` que consome SSE de `POST /v1/ai/chat` via `fetch` com `ReadableStream` | ⏳ | ~25 min |
| T4 | Renderizar tokens em streaming: última mensagem do bot atualiza caracter a caracter | ⏳ | ~20 min |
| T5 | Integrar FAB no layout de tabs (renderizado fora do navigator, posição absoluta) | ⏳ | ~15 min |

## Contrato de saída

- FAB visível em todas as 4 tabs
- Chat abre como modal/screen full-screen
- Resposta aparece token por token
- Histórico persiste enquanto o app está aberto

## Referência visual

`docs/architecture/rn-screens.html` (FAB verde + tela Copilot)
