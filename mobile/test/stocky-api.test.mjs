import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  ApiError,
  createStockyApiClient,
  normalizeApiBaseUrl,
} from "../src/lib/stocky-api.js";

function makeFetch(responses, calls = []) {
  return async (url, init = {}) => {
    calls.push({ url, init });
    const next = responses.shift();
    if (!next) {
      throw new Error(`Unexpected request: ${url}`);
    }
    return {
      ok: next.ok ?? true,
      status: next.status ?? 200,
      async json() {
        return next.body;
      },
    };
  };
}

describe("normalizeApiBaseUrl", () => {
  it("removes trailing slashes", () => {
    assert.equal(normalizeApiBaseUrl("https://api.stocky.test///"), "https://api.stocky.test");
  });

  it("rejects an empty API URL", () => {
    assert.throws(() => normalizeApiBaseUrl("  "), /API URL/);
  });
});

describe("createStockyApiClient", () => {
  it("logs in and persists the returned access token", async () => {
    const stored = [];
    const api = createStockyApiClient({
      baseUrl: "https://api.stocky.test",
      fetchImpl: makeFetch([
        {
          body: {
            access_token: "jwt-123",
            refresh_token: "refresh-123",
            user: { id: "u1", email: "op@example.com", nome: "Operador", role: "operador" },
          },
        },
      ]),
      onTokenChange: (token) => stored.push(token),
    });

    const session = await api.login({ email: "op@example.com", senha: "secret123" });

    assert.equal(session.access_token, "jwt-123");
    assert.deepEqual(stored, ["jwt-123"]);
  });

  it("sends the Bearer token on protected requests", async () => {
    const calls = [];
    const api = createStockyApiClient({
      baseUrl: "https://api.stocky.test/",
      token: "jwt-abc",
      fetchImpl: makeFetch([{ body: [{ produto_id: "p1", nome: "Arroz", quantidade_atual: 8 }] }], calls),
    });

    const estoque = await api.listStock();

    assert.equal(calls[0].url, "https://api.stocky.test/estoque");
    assert.equal(calls[0].init.headers.Authorization, "Bearer jwt-abc");
    assert.equal(estoque[0].nome, "Arroz");
  });

  it("posts movement payloads to the backend contract", async () => {
    const calls = [];
    const api = createStockyApiClient({
      baseUrl: "https://api.stocky.test",
      token: "jwt-abc",
      fetchImpl: makeFetch([{ status: 201, body: { id: "m1", produto_id: "p1", tipo: "entrada", quantidade: 5 } }], calls),
    });

    await api.createMovement({
      produto_id: "p1",
      tipo: "entrada",
      quantidade: 5,
      observacao: "NF 10",
    });

    assert.equal(calls[0].url, "https://api.stocky.test/movimentacoes");
    assert.equal(calls[0].init.method, "POST");
    assert.deepEqual(JSON.parse(calls[0].init.body), {
      produto_id: "p1",
      tipo: "entrada",
      quantidade: 5,
      observacao: "NF 10",
    });
  });

  it("gets the admin financial summary", async () => {
    const calls = [];
    const api = createStockyApiClient({
      baseUrl: "https://api.stocky.test",
      token: "jwt-admin",
      fetchImpl: makeFetch([
        {
          body: {
            total_custo_estoque: "120.50",
            total_valor_estoque: "210.00",
            margem_potencial: "89.50",
            produtos_abaixo_minimo: 2,
            total_produtos: 10,
            total_movimentacoes: 35,
          },
        },
      ], calls),
    });

    const summary = await api.getFinancialSummary();

    assert.equal(calls[0].url, "https://api.stocky.test/financeiro/resumo");
    assert.equal(calls[0].init.headers.Authorization, "Bearer jwt-admin");
    assert.equal(summary.margem_potencial, "89.50");
  });

  it("gets stored AI insights when the backend endpoint exists", async () => {
    const calls = [];
    const api = createStockyApiClient({
      baseUrl: "https://api.stocky.test",
      token: "jwt-admin",
      fetchImpl: makeFetch([
        {
          body: [
            {
              id: "i1",
              tipo: "estoque",
              titulo: "Reposição crítica",
              resumo: "Arroz está abaixo do mínimo.",
            },
          ],
        },
      ], calls),
    });

    const insights = await api.listAiInsights();

    assert.equal(calls[0].url, "https://api.stocky.test/ai/insights");
    assert.equal(insights[0].tipo, "estoque");
  });

  it("raises ApiError with backend details on non-2xx responses", async () => {
    const api = createStockyApiClient({
      baseUrl: "https://api.stocky.test",
      fetchImpl: makeFetch([{ ok: false, status: 403, body: { detail: "Acesso negado" } }]),
    });

    await assert.rejects(() => api.listProducts(), (error) => {
      assert.ok(error instanceof ApiError);
      assert.equal(error.status, 403);
      assert.equal(error.message, "Acesso negado");
      return true;
    });
  });
});
