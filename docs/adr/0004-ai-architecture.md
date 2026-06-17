# ADR 0004 - Arquitetura de IA

Status: aceito
Data: 2026-05-28
Indice: [ADR](../ADR.md)

## Contexto

Stocky precisa de insights proativos e chat reativo. Esses fluxos tem requisitos diferentes de latencia, custo e confiabilidade.

## Decisao

Separar IA em dois fluxos:

- Agentes ambientes rodam por eventos de banco ou agendamentos e gravam saidas estruturadas em logs de IA.
- Chat RAG recupera contexto relevante via pgvector e transmite resposta ao cliente.

A UI consome logs de IA armazenados para insights. Ela nao deve esperar trabalho longo de agente dentro de requests normais.

## Consequencias

- Insights sao auditaveis.
- Chat fica com menor latencia.
- Falhas de agente nao bloqueiam fluxos centrais de estoque.
- Os mesmos logs de IA podem alimentar dashboards, alertas e retrieval.
