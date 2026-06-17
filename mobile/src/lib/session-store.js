import * as SecureStore from "expo-secure-store";

const TOKEN_KEY = "stocky.accessToken";
const API_URL_KEY = "stocky.apiUrl";

export async function loadSession() {
  const [token, apiUrl] = await Promise.all([
    SecureStore.getItemAsync(TOKEN_KEY),
    SecureStore.getItemAsync(API_URL_KEY),
  ]);
  return { token: token || "", apiUrl: apiUrl || "" };
}

export async function saveToken(token) {
  if (token) {
    await SecureStore.setItemAsync(TOKEN_KEY, token);
  } else {
    await SecureStore.deleteItemAsync(TOKEN_KEY);
  }
}

export async function saveApiUrl(apiUrl) {
  if (apiUrl) {
    await SecureStore.setItemAsync(API_URL_KEY, apiUrl);
  } else {
    await SecureStore.deleteItemAsync(API_URL_KEY);
  }
}

export async function clearSession() {
  await Promise.all([
    SecureStore.deleteItemAsync(TOKEN_KEY),
    SecureStore.deleteItemAsync(API_URL_KEY),
  ]);
}
