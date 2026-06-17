import assert from "node:assert/strict";
import { describe, it } from "node:test";

import { buildLocalStockInsights, formatCurrency } from "../src/lib/view-models.js";

describe("formatCurrency", () => {
  it("formats backend decimal strings as BRL", () => {
    assert.equal(formatCurrency("1234.5"), "R$ 1.234,50");
  });
});

describe("buildLocalStockInsights", () => {
  it("creates an explicit local stock insight for low stock items", () => {
    const insights = buildLocalStockInsights([
      {
        produto_id: "p1",
        nome: "Arroz",
        quantidade_atual: 4,
        estoque_minimo: 10,
        unidade: "un",
        abaixo_minimo: true,
      },
    ]);

    assert.equal(insights.length, 1);
    assert.equal(insights[0].source, "local");
    assert.match(insights[0].resumo, /Arroz/);
    assert.match(insights[0].resumo, /4 un/);
  });
});
