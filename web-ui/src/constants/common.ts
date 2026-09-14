// ⚡ Bolt Performance Optimization:
// A shared, immutable empty array used to prevent unnecessary React component re-renders
// when returning empty array fallbacks from Zustand selectors.
export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];
