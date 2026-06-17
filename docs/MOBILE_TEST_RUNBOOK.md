# Stocky Mobile Test Runbook

Guia rapido para subir o ambiente local e testar o app mobile no celular.

## Usuarios de teste

Senha para todos os usuarios de teste: `Stocky123!`

| Papel | Email | Uso esperado |
|---|---|---|
| Admin | `admin@stocky.local` | Estoque, financeiro e IA. |
| Operador | `operador@stocky.local` | Estoque, movimentacoes, alertas e IA operacional. |

Esses usuarios sao criados ou atualizados pelo script `scripts/seed_test_data.py`.

## Terminal 1 - Supabase e backend

Execute na raiz do repositorio:

```powershell
supabase start --ignore-health-check
supabase migration up
```

Carregue as variaveis locais emitidas pelo Supabase CLI no processo atual:

```powershell
supabase status -o env | ForEach-Object {
  if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=(.*)$') {
    [Environment]::SetEnvironmentVariable($matches[1], $matches[2].Trim('"'), 'Process')
  }
}
```

Crie ou confirme os usuarios de teste e um `ai_log`:

```powershell
.\.venv\Scripts\python.exe scripts\seed_test_data.py
```

Suba o backend acessivel pela rede local:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.app:app --app-dir backend --host 0.0.0.0 --port 8500
```

Valide no navegador ou PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8500/health
```

O retorno esperado e:

```text
status
------
ok
```

## Descobrir IP do PC para celular fisico

No Windows, rode:

```powershell
ipconfig
```

Use o IPv4 da rede em que o celular tambem esta conectado. Exemplo:

```text
http://192.168.0.235:8500
```

Nao use `127.0.0.1` no celular fisico. Esse endereco aponta para o proprio celular, nao para o PC.

## Terminal 2 - App mobile

Execute em outro terminal:

```powershell
cd mobile
npm install
$env:EXPO_PUBLIC_STOCKY_API_URL="http://<IP_DO_PC>:8500"
npm run start -- --host lan
```

Exemplo com IP local:

```powershell
$env:EXPO_PUBLIC_STOCKY_API_URL="http://192.168.0.235:8500"
npm run start -- --host lan
```

Abra o Expo Go no celular e escaneie o QR code.

## Checklist de teste mobile

- Login com `admin@stocky.local`.
- Aba Estoque carrega produtos e quantidades.
- Aba Financeiro carrega resumo para admin.
- Aba IA mostra o insight persistido em `ai_logs`.
- Login com `operador@stocky.local`.
- Operador visualiza estoque, alertas e IA operacional.
- Criar uma movimentacao textual na aba Movimentacoes.

## Problemas comuns

- Se o celular nao conecta, confirme que PC e celular estao na mesma rede.
- Se o Windows Firewall perguntar, permita Python e Node em redes privadas.
- Se o backend reclamar de variaveis Supabase, rode novamente o bloco `supabase status -o env`.
- Se `/ai/insights` voltar vazio, rode novamente `scripts/seed_test_data.py`.
