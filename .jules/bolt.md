## 2023-11-20 - Prevent Unnecessary Re-Renders in Zustand Selectors
**Learning:** Returning fresh array references (`[]`) as fallback values inside Zustand selectors completely breaks memoization, causing components to re-render constantly even when the intended state hasn't changed.
**Action:** Use a globally stable reference `export const EMPTY_ARRAY = Object.freeze([]) as never[];` as the fallback in selectors for arrays to maintain referential equality and preserve React performance.
