fn main() {
    let builtin_env = "";
    let registry_env_var: Option<&str> = None;
    if builtin_env.is_empty() && registry_env_var.is_none_or(str::is_empty) {
        println!("Match!");
    } else {
        println!("No match!");
    }
}
