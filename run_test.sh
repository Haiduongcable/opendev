export OPENAI_API_KEY="sk-1234"
cargo test -p opendev-models --lib config::tests::test_get_api_key_custom_provider_openai_env_fallback
