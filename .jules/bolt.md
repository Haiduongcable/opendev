## 2024-05-18 - Zustand Selector Anti-pattern
**Learning:** Returning a full state object via `useStore(state => state)` or not providing a selector at all `useStore()` causes the component to subscribe to all state changes, resulting in frequent and unnecessary re-renders.
**Action:** Always use atomic selectors like `useStore(state => state.property)` or wrap object returns with `useShallow` from `zustand/react/shallow` when accessing multiple properties from a Zustand store.
