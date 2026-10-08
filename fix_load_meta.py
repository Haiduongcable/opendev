import sys

with open("crates/opendev-agents/src/memory_consolidation.rs", "r") as f:
    content = f.read()

# Replace load_meta body with an async one, but keep a sync version for should_consolidate
search_load_meta = '''fn load_meta(path: &Path) -> ConsolidationMeta {
    std::fs::read_to_string(path)
        .ok()
        .and_then(|s| serde_json::from_str(&s).ok())
        .unwrap_or_default()
}'''

replace_load_meta = '''fn load_meta_sync(path: &Path) -> ConsolidationMeta {
    std::fs::read_to_string(path)
        .ok()
        .and_then(|s| serde_json::from_str(&s).ok())
        .unwrap_or_default()
}

async fn load_meta(path: &Path) -> ConsolidationMeta {
    tokio::fs::read_to_string(path)
        .await
        .ok()
        .and_then(|s| serde_json::from_str(&s).ok())
        .unwrap_or_default()
}'''

content = content.replace(search_load_meta, replace_load_meta)

content = content.replace("    let meta = load_meta(&meta_path);", "    let meta = load_meta_sync(&meta_path);")
content = content.replace("    let mut meta = load_meta(&meta_path);", "    let mut meta = load_meta(&meta_path).await;")


# Fix regenerate_index path.is_file()
search_regen_index = '''    for entry in entries.flatten() {
        let path = entry.path();
        if !path.is_file() {
            continue;
        }'''
replace_regen_index = '''    while let Ok(Some(entry)) = entries.next_entry().await {
        let path = entry.path();
        if !entry.file_type().await.map(|ft| ft.is_file()).unwrap_or(false) {
            continue;
        }'''
content = content.replace(search_regen_index, replace_regen_index)

# Update test_load_save_meta
with open("crates/opendev-agents/src/memory_consolidation_tests.rs", "r") as t:
    test_content = t.read()

test_content = test_content.replace("    let meta = load_meta(&meta_path);", "    let meta = load_meta(&meta_path).await;")
test_content = test_content.replace("    let loaded = load_meta(&meta_path);", "    let loaded = load_meta(&meta_path).await;")

with open("crates/opendev-agents/src/memory_consolidation.rs", "w") as f:
    f.write(content)

with open("crates/opendev-agents/src/memory_consolidation_tests.rs", "w") as t:
    t.write(test_content)
