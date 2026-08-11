# Unset the offending env var that is causing the test to fail
unset UNKNOWN_TEST_PROVIDER_123_API_KEY
cargo test -p opendev-models --lib config::tests::test_get_api_key_custom_provider_openai_env_fallback
