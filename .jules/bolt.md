## 2026-08-24 - Zustand Component Re-render Optimization
**Learning:** Returning fresh objects or arrays (like `[]`) inside Zustand selectors circumvents strict equality checks and causes unnecessary component re-renders.
**Action:** Use a shared constant like `EMPTY_ARRAY` for array fallbacks in selectors and use atomic selectors instead of returning the whole state.
