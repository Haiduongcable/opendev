with open('crates/opendev-agents/src/react_loop/phases/llm_call_tests.rs', 'r') as f:
    content = f.read()

content = content.replace(
    'Err(Some(LoopAction::Return(Box::new(Err(AgentError::LlmError(msg.to_string())))))) => {',
    'Err(Some(LoopAction::Return(b))) => {\n            let Err(AgentError::LlmError(msg)) = *b else { panic!("Expected LlmError") };'
)

with open('crates/opendev-agents/src/react_loop/phases/llm_call_tests.rs', 'w') as f:
    f.write(content)
