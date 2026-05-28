# Sprint 18 — React Native: Fluxo de Movimentações

**Pré-requisito:** Sprint 17 (tabs) + Sprint 10 (`POST /v1/movements`, `GET /v1/products/lookup`)

## Objetivo

Fluxo completo de registro de movimentação: tipo → identificar produto → confirmar quantidade.

## Fluxo

```
1. Escolher tipo: Entrada | Saída | Ajuste
2. Identificar produto (4 opções):
   a. Scan código de barras/QR  →  GET /v1/products/lookup?barcode=...
   b. Foto do produto           →  POST /v1/products/lookup (multipart) → Gemini Vision
   c. Busca por nome/SKU        →  GET /v1/products?search=...
   d. Últimas movimentações     →  tap para repetir
3. Confirmar: quantidade + nota opcional
4. POST /v1/movements  →  feedback de sucesso
```

## Tasks

| Task | Descrição | Tag | Status | Estimativa |
|---|---|---|---|---|
| T1 | Screen `MovimentacaoTipoScreen`: 3 botões Entrada/Saída/Ajuste | `frontend` | ⏳ | ~15 min |
| T2 | Screen `IdentificarProdutoScreen`: 4 métodos como tabs/botões | `frontend` | ⏳ | ~20 min |
| T3 | Scan barcode: `expo-barcode-scanner` → `GET /v1/products/lookup?barcode=` → exibe produto encontrado | `frontend` | ⏳ | ~30 min |
| T4 | Foto produto: `expo-image-picker` → `POST /v1/products/lookup` (multipart) → exibe match Gemini | `frontend` | ⏳ | ~35 min |
| T5 | Busca texto: input com debounce → `GET /v1/products?search=` → lista selecionável | `frontend` | ⏳ | ~20 min |
| T6 | Últimas movimentações: lista das últimas 10 de `GET /v1/movements` → tap seleciona produto | `frontend` | ⏳ | ~15 min |
| T7 | Screen `ConfirmarMovimentacaoScreen`: input quantidade + nota + botão confirmar → `POST /v1/movements` | `frontend` | ⏳ | ~25 min |
| T8 | Feedback: toast de sucesso + navegação de volta para tab Movimentações | `frontend` | ⏳ | ~10 min |

## Contrato de saída

- Fluxo completo funciona para todos os 4 métodos de identificação
- Barcode scan abre câmera e retorna produto em < 2s
- Foto via Gemini retorna match em < 5s
- `POST /v1/movements` grava no DB e dispara webhook (EstoqueAgent)

## Referência visual

`docs/architecture/rn-screens.html` (tab Movimentações + sub-fluxo)

## Próximo sprint
[[phase_7/sprint_19_mobile_copilot]]
