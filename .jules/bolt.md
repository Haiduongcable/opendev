## 2024-05-24 - [Avoid dynamic array allocations in Zustand selectors]
**Learning:** [Zustand strict-equality checks fail on dynamic object/array creation leading to unnecessary re-renders in consumer components.]
**Action:** [Use a shared stable frozen `EMPTY_ARRAY` constant globally for empty arrays in Zustand hooks.]
