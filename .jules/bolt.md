## 2024-05-14 - Repository Pollution from Frontend Builds

**Learning:** Running `npm run build` in the `web-ui` directory outputs compiled assets directly into `crates/opendev-web/static/`. These files will pollute the Git index and PR if not intentionally avoided or reverted. Throwaway shell scripts used during development should also be removed.

**Action:** Always verify `git status` after frontend builds. Avoid committing `crates/opendev-web/static/*` changes unless the deployment strategy explicitly requires static assets to be version-controlled, and ensure any temporary `.sh` scripts are deleted before committing.

## 2024-05-14 - Rust async_trait Double Must Use Warnings

**Learning:** When using the `#[async_trait]` macro on traits that return types already marked as `#[must_use]` (like `Result`), newer versions of Clippy may trigger the `clippy::double_must_use` warning because the macro also automatically adds `#[must_use]` to the generated future.

**Action:** Add `#[allow(clippy::double_must_use)]` above the affected trait declarations when using `#[async_trait]` to prevent CI build failures.

## 2024-05-14 - Handling result_large_err Refactors

**Learning:** When boxing large error types (like `LoopAction` becoming `Box<LoopAction>`) to fix `clippy::result_large_err`, simply changing the method signatures isn't enough. You must also update downstream pattern matching blocks to dereference the boxed value (e.g., `match *err`) and adjust `.map_err()` closures accordingly in test files (e.g., `.map_err(|e| Some(*e))`).

**Action:** Be thorough when boxing enum variants in `Result` types. Always follow the compiler and clippy warnings to fix all downstream usages of the modified error type.
