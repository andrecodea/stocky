export class ApiError extends Error {
  constructor(message, status, body) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

export function normalizeApiBaseUrl(value) {
  const baseUrl = String(value || "").trim().replace(/\/+$/, "");
  if (!baseUrl) {
    throw new Error("API URL is required");
  }
  return baseUrl;
}

function buildHeaders(token, extra = {}) {
  const headers = {
    Accept: "application/json",
    ...extra,
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}

async function parseJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function errorMessage(body, fallback) {
  if (body && typeof body.detail === "string") {
    return body.detail;
  }
  if (Array.isArray(body?.detail)) {
    return body.detail.map((item) => item.msg || item.message || "Erro de validação").join("; ");
  }
  return fallback;
}

export function createStockyApiClient({
  baseUrl,
  token = "",
  fetchImpl = globalThis.fetch,
  onTokenChange = () => {},
} = {}) {
  const root = normalizeApiBaseUrl(baseUrl);
  let accessToken = token;

  async function request(path, { method = "GET", body, authenticated = true } = {}) {
    const response = await fetchImpl(`${root}${path}`, {
      method,
      headers: buildHeaders(authenticated ? accessToken : "", body ? { "Content-Type": "application/json" } : {}),
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await parseJson(response);

    if (!response.ok) {
      throw new ApiError(errorMessage(data, `Erro HTTP ${response.status}`), response.status, data);
    }

    return data;
  }

  return {
    get token() {
      return accessToken;
    },

    setToken(nextToken) {
      accessToken = nextToken || "";
      onTokenChange(accessToken);
    },

    async login(credentials) {
      const session = await request("/auth/login", {
        method: "POST",
        body: credentials,
        authenticated: false,
      });
      accessToken = session?.access_token || "";
      onTokenChange(accessToken);
      return session;
    },

    async listProducts() {
      return request("/produtos");
    },

    async listStock() {
      return request("/estoque");
    },

    async listAlerts() {
      return request("/estoque/alertas");
    },

    async listMovements() {
      return request("/movimentacoes");
    },

    async getFinancialSummary() {
      return request("/financeiro/resumo");
    },

    async listAiInsights() {
      return request("/ai/insights");
    },

    async createMovement(payload) {
      return request("/movimentacoes", {
        method: "POST",
        body: payload,
      });
    },

    async me() {
      return request("/perfis/me");
    },
  };
}
