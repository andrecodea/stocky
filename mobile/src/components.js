import { MaterialIcons } from "@expo/vector-icons";
import { ActivityIndicator, Pressable, StyleSheet, Text, TextInput, View } from "react-native";

import { colors, spacing } from "./theme.js";

export function Screen({ title, right, children }) {
  return (
    <View style={styles.screen}>
      <View style={styles.appBar}>
        <Text style={styles.title}>{title}</Text>
        {right}
      </View>
      <View style={styles.body}>{children}</View>
    </View>
  );
}

export function SectionLabel({ children }) {
  return <Text style={styles.sectionLabel}>{children}</Text>;
}

export function Card({ children, style }) {
  return <View style={[styles.card, style]}>{children}</View>;
}

export function IconButton({ icon, onPress, color = colors.muted, disabled = false }) {
  return (
    <Pressable onPress={onPress} disabled={disabled} style={styles.iconButton}>
      <MaterialIcons name={icon} size={22} color={disabled ? colors.faint : color} />
    </Pressable>
  );
}

export function PrimaryButton({ children, icon, onPress, loading = false, disabled = false }) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || loading}
      style={[styles.primaryButton, (disabled || loading) && styles.disabledButton]}
    >
      {loading ? <ActivityIndicator color={colors.bg} /> : icon ? <MaterialIcons name={icon} size={18} color={colors.bg} /> : null}
      <Text style={styles.primaryButtonText}>{children}</Text>
    </Pressable>
  );
}

export function SecondaryButton({ children, onPress }) {
  return (
    <Pressable onPress={onPress} style={styles.secondaryButton}>
      <Text style={styles.secondaryButtonText}>{children}</Text>
    </Pressable>
  );
}

export function Field({ label, value, onChangeText, placeholder, secureTextEntry, keyboardType = "default", autoCapitalize = "none" }) {
  return (
    <View style={styles.field}>
      <Text style={styles.fieldLabel}>{label}</Text>
      <TextInput
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={colors.faint}
        secureTextEntry={secureTextEntry}
        keyboardType={keyboardType}
        autoCapitalize={autoCapitalize}
        style={styles.input}
      />
    </View>
  );
}

export function EmptyState({ icon = "inventory-2", title, detail }) {
  return (
    <Card style={styles.empty}>
      <MaterialIcons name={icon} size={28} color={colors.faint} />
      <Text style={styles.emptyTitle}>{title}</Text>
      {detail ? <Text style={styles.emptyDetail}>{detail}</Text> : null}
    </Card>
  );
}

export function ErrorBanner({ message, onRetry }) {
  if (!message) return null;
  return (
    <View style={styles.errorBanner}>
      <MaterialIcons name="error-outline" size={18} color={colors.red} />
      <Text style={styles.errorText}>{message}</Text>
      {onRetry ? <IconButton icon="refresh" onPress={onRetry} color={colors.red} /> : null}
    </View>
  );
}

export const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: colors.bg,
  },
  appBar: {
    minHeight: 58,
    paddingHorizontal: spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    backgroundColor: colors.surface,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  title: {
    color: colors.text,
    fontSize: 18,
    fontWeight: "800",
  },
  body: {
    flex: 1,
    padding: spacing.lg,
    gap: spacing.md,
  },
  sectionLabel: {
    color: colors.faint,
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 1,
    textTransform: "uppercase",
    marginTop: spacing.xs,
  },
  card: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderWidth: 1,
    borderRadius: 8,
    padding: spacing.md,
  },
  iconButton: {
    width: 38,
    height: 38,
    alignItems: "center",
    justifyContent: "center",
  },
  primaryButton: {
    minHeight: 48,
    borderRadius: 8,
    backgroundColor: colors.green,
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row",
    gap: spacing.sm,
    paddingHorizontal: spacing.lg,
  },
  primaryButtonText: {
    color: colors.bg,
    fontSize: 14,
    fontWeight: "800",
  },
  secondaryButton: {
    minHeight: 46,
    borderRadius: 8,
    borderColor: colors.border,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: spacing.lg,
  },
  secondaryButtonText: {
    color: colors.muted,
    fontSize: 14,
    fontWeight: "700",
  },
  disabledButton: {
    opacity: 0.5,
  },
  field: {
    gap: spacing.xs,
  },
  fieldLabel: {
    color: colors.muted,
    fontSize: 12,
    fontWeight: "700",
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
  empty: {
    alignItems: "center",
    gap: spacing.sm,
    paddingVertical: spacing.xl,
  },
  emptyTitle: {
    color: colors.text,
    fontSize: 14,
    fontWeight: "800",
  },
  emptyDetail: {
    color: colors.muted,
    textAlign: "center",
    fontSize: 12,
    lineHeight: 18,
  },
  errorBanner: {
    flexDirection: "row",
    alignItems: "center",
    gap: spacing.sm,
    borderRadius: 8,
    borderColor: colors.redDark,
    borderWidth: 1,
    backgroundColor: "#180d0d",
    paddingLeft: spacing.md,
  },
  errorText: {
    flex: 1,
    color: colors.red,
    fontSize: 12,
    lineHeight: 18,
  },
});
