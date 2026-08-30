/**
 * A stable reference to an empty array to be used as a fallback in Zustand selectors.
 *
 * ⚡ Bolt Performance Optimization:
 * Returning a new inline array (e.g., `return []`) inside a Zustand selector creates a new object
 * reference on every store update. This circumvents Zustand's strict equality checks and causes
 * React to re-render the component unnecessarily, even if the actual data hasn't changed.
 * Using this stable `EMPTY_ARRAY` reference prevents these wasted render cycles.
 *
 * Expected Impact: Reduces unnecessary component re-renders when the chat store updates.
 */
export const EMPTY_ARRAY: never[] = Object.freeze([]) as never[];
