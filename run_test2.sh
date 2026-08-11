export OPENAI_API_KEY=""
export UNKNOWN_TEST_PROVIDER_123_API_KEY="sk-123"
cargo test -p opendev-models --lib config::tests::test_get_api_key_custom_provider_openai_env_fallback
