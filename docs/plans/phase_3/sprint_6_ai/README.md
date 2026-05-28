# Sprint 6 — AI: LangChain + OpenRouter

**Dev:** Backend Dev 1 (API + IA)  
**Duração estimada:** ~4–5 dias (semana 3)  
**Pré-requisito:** Sprint 4 concluído (endpoints de estoque funcionando)

## Objetivo POC

Integrar LangChain com OpenRouter para entregar **3 features de IA demonstráveis**:
1. Recomendação de reposição baseada no estoque atual
2. Chat com agente de estoque (histórico, busca web via Tavily)
3. Identificação de produto por foto (OCR/visão)

## Tasks

| Task | Arquivo | Dev | Status | Estimativa |
|------|---------|-----|--------|------------|
| T1 | [T1.md](T1.md) | API Dev 1 | ✅ | ~30 min |
| T2 | [T2.md](T2.md) | API Dev 1 | ✅ | ~40 min |
| T3 | [T3.md](T3.md) | API Dev 1 | 🔄 | ~35 min |

## Contrato de saída

- `POST /ia/recomendar-reposicao` retorna JSON com produtos e quantidades sugeridas
- `POST /ia/chat` aceita mensagem + histórico, retorna resposta do agente
- `POST /ia/identificar-produto` aceita imagem, retorna nome + campos extraídos
- Modelo de linguagem configurável via `.env` (sem hardcode)

## Próximo sprint
[[phase_3/sprint_8_frontend_conn]] — Frontend conecta estes endpoints.
