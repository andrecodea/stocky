import { MaterialIcons } from "@expo/vector-icons";
import { StatusBar } from "expo-status-bar";
import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  RefreshControl,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";

import {
  Card,
  EmptyState,
  ErrorBanner,
  Field,
  IconButton,
  PrimaryButton,
  Screen,
  SecondaryButton,
  SectionLabel,
} from "./src/components.js";
import { clearSession, loadSession, saveApiUrl, saveToken } from "./src/lib/session-store.js";
import { createStockyApiClient } from "./src/lib/stocky-api.js";
import {
  buildLocalStockInsights,
  formatCurrency,
  formatQuantity,
  movementLabel,
  movementSign,
  stockStatus,
  stockStatusLabel,
} from "./src/lib/view-models.js";
import { colors, spacing } from "./src/theme.js";

const DEFAULT_API_URL = process.env.EXPO_PUBLIC_STOCKY_API_URL || "http://127.0.0.1:8500";
const TABS = [
  { id: "home", label: "Home", icon: "home" },
  { id: "stock", label: "Estoque", icon: "inventory-2" },
  { id: "finance", label: "Fin.", icon: "payments" },
  { id: "ai", label: "IA", icon: "auto-awesome" },
  { id: "movements", label: "Mov.", icon: "swap-horiz" },
  { id: "alerts", label: "Alertas", icon: "notifications" },
];

export default function App() {
  const [booting, setBooting] = useState(true);
  const [apiUrl, setApiUrl] = useState(DEFAULT_API_URL);
  const [token, setToken] = useState("");
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState("home");
  const [stock, setStock] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [products, setProducts] = useState([]);
  const [movements, setMovements] = useState([]);
  const [financialSummary, setFinancialSummary] = useState(null);
  const [financeError, setFinanceError] = useState("");
  const [aiInsights, setAiInsights] = useState([]);
  const [aiError, setAiError] = useState("");
  const [aiBackendAvailable, setAiBackendAvailable] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const api = useMemo(
    () =>
      createStockyApiClient({
        baseUrl: apiUrl,
        token,
        onTokenChange: async (nextToken) => {
          setToken(nextToken);
          await saveToken(nextToken);
        },
      }),
    [apiUrl, token],
  );

  const loadData = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    setError("");
    try {
      const [nextStock, nextAlerts, nextMovements, nextProducts] = await Promise.all([
        api.listStock(),
        api.listAlerts(),
        api.listMovements(),
        api.listProducts(),
      ]);
      setStock(nextStock || []);
      setAlerts(nextAlerts || []);
      setMovements(nextMovements || []);
      setProducts(nextProducts || []);

      try {
        setFinancialSummary(await api.getFinancialSummary());
        setFinanceError("");
      } catch (err) {
        setFinancialSummary(null);
        setFinanceError(err.status === 403 ? "Resumo financeiro disponível apenas para admin." : err.message || "Resumo financeiro indisponível.");
      }

      try {
        setAiInsights(await api.listAiInsights());
        setAiBackendAvailable(true);
        setAiError("");
      } catch (err) {
        setAiInsights(buildLocalStockInsights(nextStock || []));
        setAiBackendAvailable(false);
        setAiError("Backend de IA ainda não disponível; exibindo insights locais de estoque.");
      }
    } catch (err) {
      setError(err.message || "Não foi possível carregar os dados.");
    } finally {
      setLoading(false);
    }
  }, [api, token]);

  useEffect(() => {
    let mounted = true;
    loadSession()
      .then((session) => {
        if (!mounted) return;
        if (session.apiUrl) setApiUrl(session.apiUrl);
        if (session.token) setToken(session.token);
      })
      .finally(() => mounted && setBooting(false));
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    if (!booting && token) {
      loadData();
    }
  }, [booting, token, loadData]);

  async function handleLogin({ email, senha, url }) {
    const cleanUrl = url.trim();
    setApiUrl(cleanUrl);
    await saveApiUrl(cleanUrl);
    const loginApi = createStockyApiClient({
      baseUrl: cleanUrl,
      onTokenChange: async (nextToken) => {
        setToken(nextToken);
        await saveToken(nextToken);
      },
    });
    const session = await loginApi.login({ email, senha });
    setUser(session.user);
    setActiveTab("home");
  }

  async function handleLogout() {
    await clearSession();
    setToken("");
    setUser(null);
    setStock([]);
    setAlerts([]);
    setProducts([]);
    setMovements([]);
    setFinancialSummary(null);
    setAiInsights([]);
  }

  if (booting) {
    return (
      <SafeAreaView style={styles.safe}>
        <StatusBar style="light" />
        <View style={styles.centered}>
          <ActivityIndicator color={colors.green} />
          <Text style={styles.bootText}>Carregando Stocky</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!token) {
    return (
      <SafeAreaView style={styles.safe}>
        <StatusBar style="light" />
        <LoginScreen defaultApiUrl={apiUrl} onLogin={handleLogin} />
      </SafeAreaView>
    );
  }

  const commonProps = {
    api,
    stock,
    alerts,
    products,
    movements,
    loading,
    error,
    onRefresh: loadData,
    financialSummary,
    financeError,
    aiInsights,
    aiError,
    aiBackendAvailable,
  };

  return (
    <SafeAreaView style={styles.safe}>
      <StatusBar style="light" />
      <View style={styles.shell}>
        {activeTab === "home" ? (
          <HomeScreen {...commonProps} user={user} onLogout={handleLogout} />
        ) : null}
        {activeTab === "stock" ? <StockScreen {...commonProps} /> : null}
        {activeTab === "finance" ? <FinanceScreen {...commonProps} /> : null}
        {activeTab === "ai" ? <AiScreen {...commonProps} /> : null}
        {activeTab === "movements" ? <MovementsScreen {...commonProps} onCreated={loadData} /> : null}
        {activeTab === "alerts" ? <AlertsScreen {...commonProps} /> : null}
        <BottomTabs activeTab={activeTab} onChange={setActiveTab} alertCount={alerts.length} />
      </View>
    </SafeAreaView>
  );
}

function LoginScreen({ defaultApiUrl, onLogin }) {
  const [apiUrl, setApiUrl] = useState(defaultApiUrl);
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit() {
    setLoading(true);
    setError("");
    try {
      await onLogin({ email: email.trim(), senha, url: apiUrl });
    } catch (err) {
      setError(err.message || "Login falhou.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <KeyboardAvoidingView style={styles.login} behavior={Platform.OS === "ios" ? "padding" : undefined}>
      <View style={styles.brandMark}>
        <MaterialIcons name="inventory-2" size={30} color={colors.green} />
      </View>
      <Text style={styles.loginTitle}>Stocky</Text>
      <Text style={styles.loginSubtitle}>Operação de estoque no mobile</Text>
      <View style={styles.loginForm}>
        <ErrorBanner message={error} />
        <Field label="API" value={apiUrl} onChangeText={setApiUrl} placeholder="https://api.stocky.com" keyboardType="url" />
        <Field label="Email" value={email} onChangeText={setEmail} placeholder="operador@empresa.com" keyboardType="email-address" />
        <Field label="Senha" value={senha} onChangeText={setSenha} placeholder="Sua senha" secureTextEntry />
        <PrimaryButton icon="login" loading={loading} disabled={!apiUrl || !email || !senha} onPress={submit}>
          Entrar
        </PrimaryButton>
      </View>
    </KeyboardAvoidingView>
  );
}

function HomeScreen({ user, stock, alerts, movements, loading, error, onRefresh, onLogout }) {
  const totalStock = stock.reduce((sum, item) => sum + Number(item.quantidade_atual || 0), 0);
  return (
    <Screen title="Stocky" right={<IconButton icon="logout" onPress={onLogout} />}>
      <RefreshScroll loading={loading} onRefresh={onRefresh}>
        <Text style={styles.greeting}>Bom dia{user?.nome ? `, ${user.nome}` : ""}</Text>
        <ErrorBanner message={error} onRetry={onRefresh} />
        <View style={styles.kpiGrid}>
          <Kpi label="Produtos" value={String(stock.length)} icon="inventory-2" tone="green" />
          <Kpi label="Alertas" value={String(alerts.length)} icon="warning" tone={alerts.length ? "red" : "green"} />
          <Kpi label="Mov. recentes" value={String(movements.length)} icon="swap-horiz" tone="blue" />
          <Kpi label="Unidades" value={String(totalStock)} icon="pin" tone="yellow" />
        </View>
        <SectionLabel>Alertas urgentes</SectionLabel>
        {alerts.slice(0, 3).map((item) => (
          <AlertRow key={item.produto_id} item={item} />
        ))}
        {!alerts.length ? <EmptyState icon="check-circle" title="Sem alertas" detail="Nenhum produto abaixo do mínimo no momento." /> : null}
      </RefreshScroll>
    </Screen>
  );
}

function StockScreen({ stock, loading, error, onRefresh }) {
  const [query, setQuery] = useState("");
  const filtered = stock.filter((item) => {
    const text = `${item.nome || ""} ${item.sku || ""}`.toLowerCase();
    return text.includes(query.toLowerCase());
  });
  return (
    <Screen title="Estoque" right={<IconButton icon="refresh" onPress={onRefresh} disabled={loading} />}>
      <SearchBox value={query} onChangeText={setQuery} placeholder="Buscar produto ou SKU" />
      <ErrorBanner message={error} onRetry={onRefresh} />
      <FlatList
        data={filtered}
        keyExtractor={(item) => item.produto_id}
        refreshControl={<RefreshControl refreshing={loading} onRefresh={onRefresh} tintColor={colors.green} />}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => <StockRow item={item} />}
        ListEmptyComponent={<EmptyState title="Nenhum produto encontrado" detail="Atualize a lista ou ajuste a busca." />}
      />
    </Screen>
  );
}

function FinanceScreen({ financialSummary, financeError, loading, onRefresh }) {
  return (
    <Screen title="Finanças" right={<IconButton icon="refresh" onPress={onRefresh} disabled={loading} />}>
      <RefreshScroll loading={loading} onRefresh={onRefresh}>
        <ErrorBanner message={financeError} onRetry={onRefresh} />
        {financialSummary ? (
          <>
            <View style={styles.kpiGrid}>
              <Kpi label="Custo estoque" value={formatCurrency(financialSummary.total_custo_estoque)} icon="account-balance-wallet" tone="yellow" />
              <Kpi label="Valor estoque" value={formatCurrency(financialSummary.total_valor_estoque)} icon="storefront" tone="green" />
              <Kpi label="Margem potencial" value={formatCurrency(financialSummary.margem_potencial)} icon="trending-up" tone="blue" />
              <Kpi label="Abaixo mínimo" value={String(financialSummary.produtos_abaixo_minimo || 0)} icon="warning" tone={financialSummary.produtos_abaixo_minimo ? "red" : "green"} />
            </View>
            <SectionLabel>Operação</SectionLabel>
            <Card>
              <MetricLine label="Produtos cadastrados" value={String(financialSummary.total_produtos || 0)} />
              <MetricLine label="Movimentações registradas" value={String(financialSummary.total_movimentacoes || 0)} />
            </Card>
          </>
        ) : !financeError ? (
          <EmptyState icon="payments" title="Resumo financeiro indisponível" detail="Atualize a tela quando o backend estiver acessível." />
        ) : null}
      </RefreshScroll>
    </Screen>
  );
}

function AiScreen({ aiInsights, aiError, aiBackendAvailable, loading, onRefresh }) {
  return (
    <Screen title="IA" right={<IconButton icon="refresh" onPress={onRefresh} disabled={loading} />}>
      <FlatList
        data={aiInsights}
        keyExtractor={(item) => item.id}
        refreshControl={<RefreshControl refreshing={loading} onRefresh={onRefresh} tintColor={colors.green} />}
        contentContainerStyle={styles.listContent}
        ListHeaderComponent={
          <>
            <View style={[styles.aiStatus, aiBackendAvailable ? styles.aiStatusOnline : styles.aiStatusLocal]}>
              <MaterialIcons name={aiBackendAvailable ? "cloud-done" : "rule"} size={20} color={aiBackendAvailable ? colors.green : colors.yellow} />
              <Text style={styles.aiStatusText}>
                {aiBackendAvailable ? "Insights estruturados do backend" : "Fallback local baseado no estoque atual"}
              </Text>
            </View>
            <ErrorBanner message={aiError} onRetry={onRefresh} />
            <SectionLabel>Insights</SectionLabel>
          </>
        }
        renderItem={({ item }) => <InsightRow item={item} />}
        ListEmptyComponent={<EmptyState icon="auto-awesome" title="Sem insights" detail="Nenhum insight disponível para o estoque atual." />}
      />
    </Screen>
  );
}

function MovementsScreen({ api, products, movements, loading, error, onRefresh, onCreated }) {
  const [tipo, setTipo] = useState("entrada");
  const [query, setQuery] = useState("");
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [quantidade, setQuantidade] = useState("1");
  const [observacao, setObservacao] = useState("");
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState("");

  const filteredProducts = products.filter((item) => {
    const text = `${item.nome || ""} ${item.sku || ""}`.toLowerCase();
    return text.includes(query.toLowerCase());
  });

  async function submit() {
    setSaving(true);
    setFormError("");
    try {
      await api.createMovement({
        produto_id: selectedProduct.id,
        tipo,
        quantidade: Number(quantidade),
        observacao: observacao.trim() || undefined,
      });
      setSelectedProduct(null);
      setQuantidade("1");
      setObservacao("");
      setQuery("");
      await onCreated();
    } catch (err) {
      setFormError(err.message || "Não foi possível criar a movimentação.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <Screen title="Movimentações" right={<IconButton icon="refresh" onPress={onRefresh} disabled={loading} />}>
      <ScrollView
        refreshControl={<RefreshControl refreshing={loading} onRefresh={onRefresh} tintColor={colors.green} />}
        contentContainerStyle={styles.scrollContent}
      >
        <ErrorBanner message={error} onRetry={onRefresh} />
        <SectionLabel>Registrar movimentação</SectionLabel>
        <View style={styles.segmented}>
          {["entrada", "saida", "ajuste"].map((option) => (
            <Pressable key={option} onPress={() => setTipo(option)} style={[styles.segment, tipo === option && styles.segmentActive]}>
              <MaterialIcons name={option === "entrada" ? "add-circle" : option === "saida" ? "remove-circle" : "tune"} size={22} color={tipo === option ? colors.green : colors.muted} />
              <Text style={[styles.segmentText, tipo === option && styles.segmentTextActive]}>{movementLabel(option)}</Text>
            </Pressable>
          ))}
        </View>
        <SearchBox value={query} onChangeText={setQuery} placeholder="Buscar produto por nome ou SKU" />
        {selectedProduct ? (
          <Card style={styles.selectedProduct}>
            <View style={styles.rowBetween}>
              <View>
                <Text style={styles.rowTitle}>{selectedProduct.nome}</Text>
                <Text style={styles.rowMeta}>SKU: {selectedProduct.sku || "sem SKU"}</Text>
              </View>
              <IconButton icon="close" onPress={() => setSelectedProduct(null)} color={colors.green} />
            </View>
          </Card>
        ) : (
          filteredProducts.slice(0, 5).map((item) => (
            <Pressable key={item.id} onPress={() => setSelectedProduct(item)} style={styles.productPickRow}>
              <MaterialIcons name="inventory-2" size={20} color={colors.faint} />
              <View style={styles.flex}>
                <Text style={styles.rowTitle}>{item.nome}</Text>
                <Text style={styles.rowMeta}>SKU: {item.sku || "sem SKU"}</Text>
              </View>
              <MaterialIcons name="chevron-right" size={22} color={colors.faint} />
            </Pressable>
          ))
        )}
        <View style={styles.formRow}>
          <View style={styles.quantityField}>
            <Text style={styles.fieldLabel}>Quantidade</Text>
            <TextInput
              value={quantidade}
              onChangeText={setQuantidade}
              keyboardType="number-pad"
              placeholder="1"
              placeholderTextColor={colors.faint}
              style={styles.input}
            />
          </View>
          <View style={styles.flex}>
            <Text style={styles.fieldLabel}>Observação</Text>
            <TextInput
              value={observacao}
              onChangeText={setObservacao}
              placeholder="NF, lote, motivo..."
              placeholderTextColor={colors.faint}
              style={styles.input}
            />
          </View>
        </View>
        <ErrorBanner message={formError} />
        <PrimaryButton
          icon="check"
          loading={saving}
          disabled={!selectedProduct || !Number(quantidade)}
          onPress={submit}
        >
          Confirmar {movementLabel(tipo).toLowerCase()}
        </PrimaryButton>
        <SectionLabel>Histórico recente</SectionLabel>
        {movements.slice(0, 8).map((item) => (
          <MovementRow key={item.id} item={item} products={products} />
        ))}
      </ScrollView>
    </Screen>
  );
}

function AlertsScreen({ alerts, loading, error, onRefresh }) {
  return (
    <Screen title="Alertas" right={<IconButton icon="refresh" onPress={onRefresh} disabled={loading} />}>
      <ErrorBanner message={error} onRetry={onRefresh} />
      <FlatList
        data={alerts}
        keyExtractor={(item) => item.produto_id}
        refreshControl={<RefreshControl refreshing={loading} onRefresh={onRefresh} tintColor={colors.green} />}
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => <AlertRow item={item} />}
        ListEmptyComponent={<EmptyState icon="check-circle" title="Estoque saudável" detail="Nenhum produto abaixo do mínimo." />}
      />
    </Screen>
  );
}

function RefreshScroll({ children, loading, onRefresh }) {
  return (
    <ScrollView
      refreshControl={<RefreshControl refreshing={loading} onRefresh={onRefresh} tintColor={colors.green} />}
      contentContainerStyle={styles.scrollContent}
    >
      {children}
    </ScrollView>
  );
}

function BottomTabs({ activeTab, onChange, alertCount }) {
  return (
    <View style={styles.bottomTabs}>
      {TABS.map((tab) => (
        <Pressable key={tab.id} onPress={() => onChange(tab.id)} style={styles.tab}>
          <View>
            <MaterialIcons name={tab.icon} size={23} color={activeTab === tab.id ? colors.green : colors.faint} />
            {tab.id === "alerts" && alertCount ? (
              <View style={styles.badge}>
                <Text style={styles.badgeText}>{alertCount > 9 ? "9+" : alertCount}</Text>
              </View>
            ) : null}
          </View>
          <Text style={[styles.tabText, activeTab === tab.id && styles.tabTextActive]}>{tab.label}</Text>
        </Pressable>
      ))}
    </View>
  );
}

function Kpi({ label, value, icon, tone }) {
  const toneColor = tone === "red" ? colors.red : tone === "yellow" ? colors.yellow : tone === "blue" ? colors.blue : colors.green;
  return (
    <Card style={styles.kpi}>
      <View style={styles.kpiLabelRow}>
        <MaterialIcons name={icon} size={14} color={toneColor} />
        <Text style={styles.kpiLabel}>{label}</Text>
      </View>
      <Text style={[styles.kpiValue, { color: toneColor }]}>{value}</Text>
    </Card>
  );
}

function SearchBox({ value, onChangeText, placeholder }) {
  return (
    <View style={styles.searchBox}>
      <MaterialIcons name="search" size={20} color={colors.faint} />
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={colors.faint}
        style={styles.searchInput}
      />
    </View>
  );
}

function StockRow({ item }) {
  const status = stockStatus(item);
  const statusColor = status === "baixo" ? colors.red : colors.green;
  return (
    <Card style={styles.stockRow}>
      <View style={styles.rowIcon}>
        <MaterialIcons name="inventory-2" size={20} color={colors.faint} />
      </View>
      <View style={styles.flex}>
        <Text style={styles.rowTitle}>{item.nome}</Text>
        <Text style={styles.rowMeta}>
          {item.sku || "sem SKU"} · mínimo {item.estoque_minimo || 0}
        </Text>
      </View>
      <View style={styles.stockRight}>
        <Text style={styles.quantity}>{formatQuantity(item.quantidade_atual, item.unidade)}</Text>
        <Text style={[styles.statusChip, { color: statusColor }]}>{stockStatusLabel(item)}</Text>
      </View>
    </Card>
  );
}

function AlertRow({ item }) {
  return (
    <View style={styles.alertRow}>
      <MaterialIcons name="error-outline" size={22} color={colors.red} />
      <View style={styles.flex}>
        <Text style={styles.rowTitle}>{item.nome}</Text>
        <Text style={styles.rowMeta}>
          {formatQuantity(item.quantidade_atual, item.unidade)} · mínimo {item.estoque_minimo || 0}
        </Text>
      </View>
    </View>
  );
}

function MetricLine({ label, value }) {
  return (
    <View style={styles.metricLine}>
      <Text style={styles.rowMeta}>{label}</Text>
      <Text style={styles.metricLineValue}>{value}</Text>
    </View>
  );
}

function InsightRow({ item }) {
  const color = item.tipo === "financeiro" ? colors.yellow : item.tipo === "comercial" ? colors.blue : colors.green;
  return (
    <Card style={styles.insightCard}>
      <View style={styles.rowBetween}>
        <View style={[styles.insightChip, { borderColor: color }]}>
          <Text style={[styles.insightChipText, { color }]}>{item.tipo || "ia"}</Text>
        </View>
        {item.source === "local" ? <Text style={styles.localTag}>local</Text> : null}
      </View>
      <Text style={styles.rowTitle}>{item.titulo || "Insight"}</Text>
      <Text style={styles.insightText}>{item.resumo || item.conteudo || "Sem resumo disponível."}</Text>
    </Card>
  );
}

function MovementRow({ item, products }) {
  const product = products.find((p) => p.id === item.produto_id);
  const sign = movementSign(item.tipo);
  const color = item.tipo === "saida" ? colors.red : item.tipo === "ajuste" ? colors.indigo : colors.green;
  return (
    <View style={styles.movementRow}>
      <View style={[styles.movementIcon, { backgroundColor: item.tipo === "saida" ? colors.redDark : colors.greenDark }]}>
        <MaterialIcons name={item.tipo === "saida" ? "remove" : item.tipo === "ajuste" ? "tune" : "add"} size={18} color={color} />
      </View>
      <View style={styles.flex}>
        <Text style={styles.rowTitle}>{product?.nome || item.produto_id}</Text>
        <Text style={styles.rowMeta}>{movementLabel(item.tipo)} · {item.criado_em ? item.criado_em.slice(0, 16).replace("T", " ") : "sem data"}</Text>
      </View>
      <Text style={[styles.movementQty, { color }]}>
        {sign}
        {item.quantidade}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  shell: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  centered: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.md,
  },
  bootText: {
    color: colors.muted,
    fontSize: 13,
  },
  login: {
    flex: 1,
    justifyContent: "center",
    padding: spacing.xl,
    backgroundColor: colors.bg,
  },
  brandMark: {
    width: 64,
    height: 64,
    borderRadius: 18,
    backgroundColor: colors.greenDark,
    borderColor: "#235223",
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: spacing.lg,
  },
  loginTitle: {
    color: colors.text,
    fontSize: 34,
    fontWeight: "900",
  },
  loginSubtitle: {
    color: colors.muted,
    fontSize: 15,
    marginTop: spacing.xs,
    marginBottom: spacing.xl,
  },
  loginForm: {
    gap: spacing.md,
  },
  greeting: {
    color: colors.muted,
    fontSize: 15,
  },
  scrollContent: {
    gap: spacing.md,
    paddingBottom: spacing.xl,
  },
  listContent: {
    gap: spacing.md,
    paddingBottom: spacing.xl,
  },
  kpiGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: spacing.md,
  },
  kpi: {
    width: "47.8%",
    minHeight: 92,
    justifyContent: "space-between",
  },
  kpiLabelRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.xs,
  },
  kpiLabel: {
    color: colors.muted,
    fontSize: 11,
    fontWeight: "800",
    textTransform: "uppercase",
  },
  kpiValue: {
    fontSize: 28,
    fontWeight: "900",
  },
  bottomTabs: {
    minHeight: 70,
    backgroundColor: colors.surface,
    borderTopColor: colors.border,
    borderTopWidth: 1,
    flexDirection: "row",
    paddingTop: spacing.sm,
    paddingBottom: spacing.sm,
  },
  tab: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 2,
  },
  tabText: {
    color: colors.faint,
    fontSize: 11,
    fontWeight: "700",
  },
  tabTextActive: {
    color: colors.green,
  },
  badge: {
    position: "absolute",
    top: -7,
    right: -12,
    minWidth: 18,
    height: 18,
    borderRadius: 9,
    backgroundColor: colors.red,
    alignItems: "center",
    justifyContent: "center",
  },
  badgeText: {
    color: colors.text,
    fontSize: 10,
    fontWeight: "900",
  },
  searchBox: {
    minHeight: 46,
    borderRadius: 8,
    backgroundColor: colors.surface2,
    borderColor: colors.border,
    borderWidth: 1,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    paddingHorizontal: spacing.md,
  },
  searchInput: {
    flex: 1,
    color: colors.text,
    fontSize: 14,
  },
  stockRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
  },
  rowIcon: {
    width: 38,
    height: 38,
    borderRadius: 8,
    backgroundColor: colors.surface2,
    alignItems: "center",
    justifyContent: "center",
  },
  flex: {
    flex: 1,
  },
  rowTitle: {
    color: colors.text,
    fontSize: 14,
    fontWeight: "800",
  },
  rowMeta: {
    color: colors.muted,
    fontSize: 12,
    marginTop: 2,
  },
  stockRight: {
    alignItems: "flex-end",
    gap: spacing.xs,
  },
  quantity: {
    color: colors.text,
    fontSize: 13,
    fontWeight: "800",
  },
  statusChip: {
    fontSize: 11,
    fontWeight: "900",
  },
  alertRow: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: spacing.md,
    backgroundColor: "#160d0d",
    borderColor: colors.redDark,
    borderWidth: 1,
    borderRadius: 8,
    padding: spacing.md,
  },
  metricLine: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: spacing.sm,
    borderBottomColor: colors.border,
    borderBottomWidth: 1,
  },
  metricLineValue: {
    color: colors.text,
    fontSize: 14,
    fontWeight: "900",
  },
  aiStatus: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    borderRadius: 8,
    borderWidth: 1,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  aiStatusOnline: {
    backgroundColor: colors.greenDark,
    borderColor: "#245c30",
  },
  aiStatusLocal: {
    backgroundColor: colors.yellowDark,
    borderColor: "#4d3b16",
  },
  aiStatusText: {
    flex: 1,
    color: colors.text,
    fontSize: 13,
    fontWeight: "800",
  },
  insightCard: {
    gap: spacing.sm,
  },
  insightChip: {
    borderWidth: 1,
    borderRadius: 8,
    paddingHorizontal: spacing.sm,
    paddingVertical: 3,
  },
  insightChipText: {
    fontSize: 11,
    fontWeight: "900",
    textTransform: "uppercase",
  },
  localTag: {
    color: colors.yellow,
    fontSize: 11,
    fontWeight: "900",
  },
  insightText: {
    color: colors.muted,
    fontSize: 13,
    lineHeight: 19,
  },
  segmented: {
    flexDirection: "row",
    gap: spacing.sm,
  },
  segment: {
    flex: 1,
    minHeight: 72,
    borderRadius: 8,
    borderColor: colors.border,
    borderWidth: 1,
    backgroundColor: colors.surface2,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.xs,
  },
  segmentActive: {
    borderColor: "#245c30",
    backgroundColor: colors.greenDark,
  },
  segmentText: {
    color: colors.muted,
    fontSize: 12,
    fontWeight: "800",
  },
  segmentTextActive: {
    color: colors.green,
  },
  productPickRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    padding: spacing.md,
    borderRadius: 8,
    backgroundColor: colors.surface2,
    borderColor: colors.border,
    borderWidth: 1,
  },
  selectedProduct: {
    backgroundColor: colors.greenDark,
    borderColor: "#245c30",
  },
  rowBetween: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: spacing.md,
  },
  formRow: {
    flexDirection: "row",
    gap: spacing.md,
  },
  quantityField: {
    width: 104,
  },
  fieldLabel: {
    color: colors.muted,
    fontSize: 12,
    fontWeight: "700",
    marginBottom: spacing.xs,
  },
  input: {
    minHeight: 46,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: colors.border,
    color: colors.text,
    backgroundColor: colors.surface2,
    paddingHorizontal: spacing.md,
    fontSize: 14,
  },
  movementRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.md,
    padding: spacing.md,
    borderRadius: 8,
    backgroundColor: colors.surface2,
  },
  movementIcon: {
    width: 34,
    height: 34,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
  },
  movementQty: {
    fontSize: 14,
    fontWeight: "900",
  },
});
