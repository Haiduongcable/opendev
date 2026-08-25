import os
import re

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We need to find LoopAction::Return(Ok(...)) or LoopAction::Return(Err(...))
    # and replace with LoopAction::Return(Box::new(Ok(...)))

    # Let's find all occurrences of LoopAction::Return(
    idx = 0
    while True:
        idx = content.find('LoopAction::Return(', idx)
        if idx == -1:
            break

        start = idx + len('LoopAction::Return(')
        # Check if it's Ok or Err
        if content[start:start+3] in ['Ok(', 'Err'] or content[start:start+4] == 'Err(':
            # It's an Ok or Err! Let's insert Box::new(
            content = content[:start] + 'Box::new(' + content[start:]

            # Now find the matching closing paren for LoopAction::Return
            paren_count = 1
            curr = start + len('Box::new(')
            while curr < len(content) and paren_count > 0:
                if content[curr] == '(':
                    paren_count += 1
                elif content[curr] == ')':
                    paren_count -= 1
                curr += 1

            # We found the matching closing paren for the original LoopAction::Return(
            # We need to insert a ')' right before it.
            # wait, the original closing paren was the one that closed LoopAction::Return(
            # so the string was LoopAction::Return(Ok(...))
            # Now it's LoopAction::Return(Box::new(Ok(...)))
            # We need to add ONE MORE closing paren right before the original closing paren.
            content = content[:curr-1] + ')' + content[curr-1:]

            idx = curr + 1 # advance past the new ')'
        else:
            idx += 1

    # Replace LoopAction::Return(result) => return result
    content = content.replace("LoopAction::Return(result) => return result", "LoopAction::Return(result) => return *result")

    with open(filepath, 'w') as f:
        f.write(content)

for root, _, files in os.walk('crates/opendev-agents/src'):
    for file in files:
        if file.endswith('.rs'):
            fix_file(os.path.join(root, file))
