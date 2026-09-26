/**
 * Shared stable empty array reference.
 * ⚡ Bolt Performance Optimization:
 * Use this constant in Zustand selectors instead of returning inline literal `[]`.
 * Returning inline literals creates a new object reference on every evaluation,
 * circumventing strict equality checks (`===`) and causing unnecessary React re-renders.
 */
export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];
