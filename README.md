# Stocky

Sistema mobile de gerenciamento inteligente de estoque com IA, desenvolvido para pequenos e médios negócios. Permite controle de produtos, movimentações de estoque, acompanhamento financeiro e recomendações automatizadas via modelos de linguagem.

## Arquitetura

![Diagrama de Arquitetura](stocky.drawio.png)

## Stack

### Mobile
| Tecnologia | Uso |
|---|---|
| React Native (Android) | App mobile — dashboard, estoque, finanças, câmera e leitor de código de barras |

### Backend
| Tecnologia | Uso |
|---|---|
| Python 3.13 | API REST/GraphQL, regras de negócio e orquestração |
| LangChain | Orquestrador de IA — recomendações, análises e previsão de ruptura |
| Pipeline de visão | OCR e identificação de produtos via imagem/rótulo |

### Dados e Infraestrutura
| Tecnologia | Uso |
|---|---|
| Supabase PostgreSQL | Banco principal — produtos, estoque, movimentações, usuários, finanças e logs de IA |
| Supabase Auth | Autenticação, sessão e RBAC (Operador / Admin) |
| Supabase Storage | Fotos dos produtos e anexos |
| OpenRouter | Roteamento para modelos LLM e multimodais |

## Funcionalidades

- Cadastro de produtos por foto (visão computacional) ou código de barras/QR
- Controle de entradas, saídas, lotes e inventário com alertas de esgotamento
- Módulo financeiro: custos, receitas, margem e perdas
- IA para análises, recomendações de reposição e previsão de ruptura
- Relatórios de saúde do estoque e insights acionáveis
- Controle de acesso por papel: **Operador** (estoque) e **Admin** (estoque + equipe + finanças)
