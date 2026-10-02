## 2024-05-19 - Unnecessary Zustand re-renders
**Learning:** Returning new object or array references (e.g., `[]`) within Zustand selector functions circumvents strict equality checks, causing the component to re-render on every state update, even if the array contents have not changed.
**Action:** Use a shared, stable reference like `export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];` as the default fallback value in Zustand selectors.
