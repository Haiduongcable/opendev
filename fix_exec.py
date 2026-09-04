with open('crates/opendev-agents/src/react_loop/execution.rs', 'r') as f:
    content = f.read()
content = content.replace('super::types::LoopAction::Return(result) => return result,', 'super::types::LoopAction::Return(result) => return *result,')
with open('crates/opendev-agents/src/react_loop/execution.rs', 'w') as f:
    f.write(content)
