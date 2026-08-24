// ⚡ Bolt: A frozen, shared empty array reference.
// Use this as a fallback value in Zustand selectors or React hooks
// to prevent circumventing strict referential equality checks (`===`)
// that cause unnecessary component re-renders when returning `[]` dynamically.
export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];
