# Sprint 8 — Frontend: Conexão com Endpoints

**Dev:** Frontend Dev 1 (Conexão)  
**Duração estimada:** ~4–5 dias (semana 3)  
**Pré-requisito:** Sprint 7 concluído (telas com mock) + Sprint 4 concluído (endpoints estoque)

## Objetivo POC

Conectar o MVP Streamlit aos dados reais e planejar a conexão React Native → FastAPI para pós-POC.

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | Frontend Dev 1 | ✅ | ~35 min |
| T2 | [T2.md](T2.md) | Frontend Dev 1 | ✅ | ~40 min |
| T3 | [T3.md](T3.md) | Frontend Dev 1 | 🔄 | ~40 min |

## Contrato de saída (demo POC)

- ✅ Streamlit conectado ao Supabase — dados reais em dashboard e estoque
- ✅ Alertas de estoque mínimo funcionando em tempo real
- ✅ Chat IA via `answer_query()` com histórico persistente entre páginas
- 🔄 Tela de IA com `POST /ia/chat` e `POST /ia/recomendar-reposicao` via FastAPI (pendente — endpoints em construção)
- ⏳ Auth flow React Native + conexão com FastAPI — pós-POC
