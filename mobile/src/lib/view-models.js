export function stockStatus(item) {
  if (item.abaixo_minimo) {
    return "baixo";
  }
  return "ok";
}

export function stockStatusLabel(item) {
  return stockStatus(item) === "baixo" ? "Baixo" : "OK";
}

export function movementSign(tipo) {
  if (tipo === "saida") {
    return "-";
  }
  if (tipo === "ajuste") {
    return "~";
  }
  return "+";
}

export function movementLabel(tipo) {
  const labels = {
    entrada: "Entrada",
    saida: "Saída",
    ajuste: "Ajuste",
  };
  return labels[tipo] || tipo;
}

export function formatQuantity(value, unidade = "un") {
  return `${Number(value || 0)} ${unidade || "un"}`;
}

export function formatCurrency(value) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
    minimumFractionDigits: 2,
  })
    .format(Number(value || 0))
    .replace(/\u00a0/g, " ");
}

export function buildLocalStockInsights(stock = []) {
  return stock
    .filter((item) => item.abaixo_minimo)
    .map((item) => ({
      id: `local-stock-${item.produto_id}`,
      tipo: "estoque",
      titulo: "Reposição abaixo do mínimo",
      resumo: `${item.nome} está com ${formatQuantity(item.quantidade_atual, item.unidade)} e mínimo de ${item.estoque_minimo || 0}.`,
      source: "local",
      severidade: Number(item.quantidade_atual || 0) <= 0 ? "critica" : "atencao",
    }));
}
