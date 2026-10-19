use super::*;
use tempfile::tempdir;

#[tokio::test]
async fn test_parse_type_and_body() {
    let content = "---\ntype: session\n---\nHello World!";
    let (ft, body) = parse_type_and_body(content);
    assert_eq!(ft, "session");
    assert_eq!(body, "Hello World!");

    let no_fm = "Just some text";
    let (ft, body) = parse_type_and_body(no_fm);
    assert_eq!(ft, "general");
    assert_eq!(body, "Just some text");
}

#[tokio::test]
async fn test_count_session_files_empty() {
    let dir = tempdir().unwrap();
    assert_eq!(count_session_files(dir.path()).await, 0);
}

#[tokio::test]
async fn test_count_session_files_mixed() {
    let dir = tempdir().unwrap();

    // Session by name
    tokio::fs::write(
        dir.path().join("session-123.md"),
        "---\ntype: general\n---\nbody",
    )
    .await
    .unwrap();

    // Session by frontmatter
    tokio::fs::write(dir.path().join("other.md"), "---\ntype: session\n---\nbody")
        .await
        .unwrap();

    // Not a session
    tokio::fs::write(dir.path().join("notes.md"), "---\ntype: project\n---\nbody")
        .await
        .unwrap();

    // MEMORY.md is ignored
    tokio::fs::write(dir.path().join("MEMORY.md"), "# Index")
        .await
        .unwrap();

    assert_eq!(count_session_files(dir.path()).await, 2);
}

#[tokio::test]
async fn test_scan_all_memory_files() {
    let dir = tempdir().unwrap();

    tokio::fs::write(
        dir.path().join("session-1.md"),
        "---\ntype: session\n---\nOne",
    )
    .await
    .unwrap();

    tokio::fs::write(dir.path().join("notes.md"), "---\ntype: project\n---\nTwo")
        .await
        .unwrap();

    tokio::fs::write(dir.path().join("MEMORY.md"), "# Index")
        .await
        .unwrap();
    tokio::fs::write(dir.path().join("not-md.txt"), "text")
        .await
        .unwrap();

    let files = scan_all_memory_files(dir.path()).await;
    assert_eq!(files.len(), 2);

    let session = files.iter().find(|f| f.filename == "session-1.md").unwrap();
    assert_eq!(session.file_type, "session");
    assert_eq!(session.body, "One");

    let notes = files.iter().find(|f| f.filename == "notes.md").unwrap();
    assert_eq!(notes.file_type, "project");
    assert_eq!(notes.body, "Two");
}

#[tokio::test]
async fn test_load_save_meta() {
    let dir = tempdir().unwrap();
    let meta_path = dir.path().join("meta.json");

    // Load non-existent
    let meta = load_meta(&meta_path).await;
    assert!(meta.last_run.is_none());

    // Save
    let meta = ConsolidationMeta {
        last_run: Some("2024-01-01T00:00:00Z".to_string()),
        files_processed: 5,
    };
    save_meta(&meta_path, &meta).await;

    // Load back
    let loaded = load_meta(&meta_path).await;
    assert_eq!(loaded.last_run.unwrap(), "2024-01-01T00:00:00Z");
    assert_eq!(loaded.files_processed, 5);
}

#[tokio::test]
async fn test_regenerate_index() {
    let dir = tempdir().unwrap();

    tokio::fs::write(
        dir.path().join("a.md"),
        "---\ndescription: \"Alpha\"\n---\nbody",
    )
    .await
    .unwrap();

    tokio::fs::write(dir.path().join("b.md"), "---\ntype: general\n---\nno desc")
        .await
        .unwrap();

    regenerate_index(dir.path()).await.unwrap();

    let index = tokio::fs::read_to_string(dir.path().join("MEMORY.md"))
        .await
        .unwrap();
    assert!(index.contains("- [a.md](a.md) — Alpha"));
    assert!(index.contains("- [b.md](b.md)"));
    assert!(!index.contains("MEMORY.md"));
}

#[tokio::test]
async fn test_should_consolidate_no_dir() {
    let dir = tempdir().unwrap();
    // No .opendev/memory created
    assert!(!should_consolidate(dir.path()).await);
}
