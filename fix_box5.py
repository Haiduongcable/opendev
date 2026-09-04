import os
import re

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Change the enum definition
    content = content.replace(
        'Return(Result<AgentResult, AgentError>),',
        'Return(Box<Result<AgentResult, AgentError>>),'
    )

    # We will do literal replacements line by line using simple python replace
    # We know what the lines look like
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'LoopAction::Return(' in line and 'types::LoopAction::Return' not in line:
            if 'LoopAction::Return(Err(e))' in line:
                lines[i] = line.replace('LoopAction::Return(Err(e))', 'LoopAction::Return(Box::new(Err(e)))')
            elif 'LoopAction::Return(Ok(AgentResult::backgrounded(' in line:
                lines[i] = line.replace('LoopAction::Return(Ok(AgentResult::backgrounded(', 'LoopAction::Return(Box::new(Ok(AgentResult::backgrounded(')
                # add a closing paren to the end of the statement block
                j = i
                while j < len(lines):
                    if lines[j].strip().endswith(')));'):
                        lines[j] = lines[j].replace(')));', '))));')
                        break
                    elif lines[j].strip().endswith(')));'):
                        lines[j] = lines[j].replace(')));', '))));')
                        break
                    elif lines[j].strip().endswith('))));'):
                        lines[j] = lines[j].replace('))));', ')))));')
                        break
                    elif lines[j].strip().endswith('))));'):
                        lines[j] = lines[j].replace('))));', ')))));')
                        break
                    j += 1
            elif 'LoopAction::Return(Ok(AgentResult::interrupted(' in line:
                lines[i] = line.replace('LoopAction::Return(Ok(AgentResult::interrupted(', 'LoopAction::Return(Box::new(Ok(AgentResult::interrupted(')
                j = i
                while j < len(lines):
                    if lines[j].strip().endswith(')));'):
                        lines[j] = lines[j].replace(')));', '))));')
                        break
                    elif lines[j].strip().endswith('))));'):
                        lines[j] = lines[j].replace('))));', ')))));')
                        break
                    j += 1
            elif 'LoopAction::Return(Ok(result))' in line:
                lines[i] = line.replace('LoopAction::Return(Ok(result))', 'LoopAction::Return(Box::new(Ok(result)))')
            elif 'LoopAction::Return(Err(AgentError::LlmError(format!(' in line:
                lines[i] = line.replace('LoopAction::Return(Err(AgentError::LlmError(format!(', 'LoopAction::Return(Box::new(Err(AgentError::LlmError(format!(')
                j = i
                while j < len(lines):
                    if lines[j].strip().endswith(')))));'):
                        lines[j] = lines[j].replace(')))));', '))))));')
                        break
                    j += 1
            elif 'LoopAction::Return(Err(AgentError::LlmError("Empty response body".to_string())))' in line:
                lines[i] = line.replace('LoopAction::Return(Err(AgentError::LlmError("Empty response body".to_string())))', 'LoopAction::Return(Box::new(Err(AgentError::LlmError("Empty response body".to_string()))))')
            elif 'LoopAction::Return(Err(crate::traits::AgentError::Other(format!(' in line:
                lines[i] = line.replace('LoopAction::Return(Err(crate::traits::AgentError::Other(format!(', 'LoopAction::Return(Box::new(Err(crate::traits::AgentError::Other(format!(')
                j = i
                while j < len(lines):
                    if lines[j].strip().endswith('))));'):
                        lines[j] = lines[j].replace('))));', ')))));')
                        break
                    j += 1
            elif 'LoopAction::Return(Err(AgentError::LlmError(msg)))' in line:
                lines[i] = line.replace('LoopAction::Return(Err(AgentError::LlmError(msg)))', 'LoopAction::Return(Box::new(Err(AgentError::LlmError(msg))))')

        elif 'super::types::LoopAction::Return(result)' in line:
            lines[i] = line.replace('super::types::LoopAction::Return(result)', 'super::types::LoopAction::Return(result)')
            # Wait, the matching is matching `result`. If it matches `LoopAction::Return(result)`, the inner `result` is a `Box`. We don't need to wrap it in Box::new when matching.
            # actually we don't need to change `super::types::LoopAction::Return(result) => return result` unless the return type is expecting the unboxed `result`, but `run_inner` returns `LoopAction` so it expects the `result` to just be returned or unwrapped?
            # Oh, if we change LoopAction::Return to Box, then `result` bound variable is a Box. If we `return *result`, then it would unbox. Let's look at `execution.rs`.

    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

for root, _, files in os.walk('crates/opendev-agents/src'):
    for file in files:
        if file.endswith('.rs'):
            process_file(os.path.join(root, file))
