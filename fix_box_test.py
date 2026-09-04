import re
with open('crates/opendev-agents/src/react_loop/phases/llm_call_tests.rs', 'r') as f:
    content = f.read()

# the match arm expects `msg` string to be bound. It was `LoopAction::Return(Err(AgentError::LlmError(msg)))`
# now the enum holds a `Box<Result<AgentResult, AgentError>>`
# so the pattern is: `LoopAction::Return(boxed_res)`
# then we can match inside the block: `if let Err(AgentError::LlmError(msg)) = *boxed_res`
# Actually, we can use box patterns but they are unstable. Or we can just bind `b` and check inside.
# `Err(Some(LoopAction::Return(b)))`

def replace_fn(match):
    return """Err(Some(LoopAction::Return(b))) => {
        let Err(AgentError::LlmError(msg)) = *b else { panic!("Expected LlmError") };"""

content = re.sub(r'Err\(Some\(LoopAction::Return\(Box::new\(Err\(AgentError::LlmError\([^)]+\)\)\)\)\)\) => \{', replace_fn, content)

with open('crates/opendev-agents/src/react_loop/phases/llm_call_tests.rs', 'w') as f:
    f.write(content)
