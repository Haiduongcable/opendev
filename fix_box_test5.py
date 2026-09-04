import re
with open('crates/opendev-agents/src/react_loop/phases/llm_call_tests.rs', 'r') as f:
    content = f.read()

def replace_fn(match):
    return """Err(Some(LoopAction::Return(b))) => {
            let Err(AgentError::LlmError(msg)) = *b else { panic!("Expected LlmError") };"""

content = re.sub(r'Err\(Some\(LoopAction::Return\(Err\(AgentError::LlmError\(msg\)\)\)\)\) => \{', replace_fn, content)

with open('crates/opendev-agents/src/react_loop/phases/llm_call_tests.rs', 'w') as f:
    f.write(content)
