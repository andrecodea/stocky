# Sprint 8 — Frontend: Conexão com Endpoints

**Dev:** Frontend Dev 1 (Conexão)  
**Duração estimada:** ~4–5 dias (semana 3)  
**Pré-requisito:** Sprint 7 concluído (telas com mock) + Sprint 4 concluído (endpoints estoque)

## Objetivo POC

Substituir dados mockados por dados reais da API. Implementar Auth flow completo com Supabase. App demo-ready ao final.

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | Frontend Dev 1 | ⏳ | ~35 min |
| T2 | [T2.md](T2.md) | Frontend Dev 1 | ⏳ | ~40 min |
| T3 | [T3.md](T3.md) | Frontend Dev 1 | ⏳ | ~40 min |

## Contrato de saída (demo POC)

- Login com email/senha funciona — JWT salvo, sessão persiste
- `EstoqueScreen` exibe produtos reais do banco
- `AlertasScreen` exibe alertas reais via `GET /estoque/alertas`
- Tela de IA exibe recomendação gerada via `POST /ia/recomendar-reposicao`
