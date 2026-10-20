// PERF: A stable empty array reference used as a fallback in Zustand selectors to prevent unnecessary component re-renders that would otherwise occur if inline arrays (`[]`) were returned.
export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];
