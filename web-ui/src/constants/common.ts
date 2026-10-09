/**
 * A stable, shared empty array reference.
 *
 * ⚡ Bolt Optimization:
 * When using state managers like Zustand, returning `[]` as a fallback from a selector
 * creates a new array reference on every state update. This causes strict-equality checks
 * to fail and forces unnecessary React component re-renders.
 * Using `EMPTY_ARRAY` provides a stable reference, ensuring components only re-render
 * when the actual array data changes.
 *
 * Impact: Prevents O(1) unnecessary re-renders per store update for subscribed components.
 */
export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];
