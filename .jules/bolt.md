## 2024-09-14 - Stable references in Zustand selectors
**Learning:** Using `[]` inline in Zustand selectors causes the default strict equality check (`old === new`) to fail on every store update, triggering unnecessary re-renders in connected components.
**Action:** Use a shared, frozen empty array reference (`export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];`) to return from selectors when an empty array is expected.
