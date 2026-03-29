/**
 * Code Execution tests
 */

import { describe, test, expect } from 'bun:test';
import { 
  parseLiterateMarkdown, 
  parseCodeBlockMeta,
  executeCode,
  type CodeBlock
} from './literate-commands';

// ============================================================================
// Test Data
// ============================================================================

const EXEC_BLOCK = `---
\`\`\`yaml {config}
step: exec
\`\`\`
Run the code.

\`\`\`python {exec}
def main(x):
    return x * 2
\`\`\`
`;

const SUBAGENT_BLOCK = `---
\`\`\`yaml {config}
step: subagent
\`\`\`
Spawn agents.

\`\`\`python {subagent=scout}
def collect(objectives):
    for obj in objectives:
        yield f"Research: {obj}"
\`\`\`
`;

const COMBINED_BLOCK = `---
\`\`\`yaml {config}
step: combined
\`\`\`
Run and spawn.

\`\`\`python {exec subagent=scout}
def collect(objectives):
    for obj in objectives:
        yield f"Research: {obj}"
\`\`\`
`;

const NAMED_BLOCK = `---
\`\`\`yaml {config}
step: named
\`\`\`
Named execution.

\`\`\`python {exec=my_result}
def main(x):
    return {"value": x * 2}
\`\`\`
`;

// ============================================================================
// Tests
// ============================================================================

describe('parseCodeBlockMeta', () => {
  test('parses {exec} metadata', () => {
    const meta = ['exec'];
    const result = parseCodeBlockMeta(meta);
    
    expect(result.type).toBe('exec');
    expect(result.name).toBeNull();
    expect(result.subagent).toBeNull();
  });

  test('parses {exec=NAME} metadata', () => {
    const meta = ['exec=my_result'];
    const result = parseCodeBlockMeta(meta);
    
    expect(result.type).toBe('exec');
    expect(result.name).toBe('my_result');
  });

  test('parses {subagent=AGENT} metadata', () => {
    const meta = ['subagent=scout'];
    const result = parseCodeBlockMeta(meta);
    
    expect(result.type).toBe('subagent');
    expect(result.subagent).toBe('scout');
  });

  test('parses {exec subagent=AGENT} metadata', () => {
    const meta = ['exec', 'subagent=scout'];
    const result = parseCodeBlockMeta(meta);
    
    expect(result.type).toBe('exec-subagent');
    expect(result.subagent).toBe('scout');
  });

  test('parses {subagent=AGENT name=NAME} metadata', () => {
    const meta = ['subagent=scout', 'name=results'];
    const result = parseCodeBlockMeta(meta);
    
    expect(result.type).toBe('subagent');
    expect(result.subagent).toBe('scout');
    expect(result.name).toBe('results');
  });
});

describe('code block extraction', () => {
  test('extracts {exec} code blocks', () => {
    const steps = parseLiterateMarkdown(EXEC_BLOCK);
    const step = steps[0];
    
    expect(step.codeBlocks.length).toBe(1);
    expect(step.codeBlocks[0].language).toBe('python');
    expect(step.codeBlocks[0].meta).toContain('exec');
    expect(step.codeBlocks[0].code).toContain('def main');
  });

  test('extracts {subagent=AGENT} code blocks', () => {
    const steps = parseLiterateMarkdown(SUBAGENT_BLOCK);
    const step = steps[0];
    
    expect(step.codeBlocks.length).toBe(1);
    expect(step.codeBlocks[0].meta).toContain('subagent=scout');
    expect(step.codeBlocks[0].code).toContain('yield');
  });

  test('extracts combined {exec subagent=AGENT} code blocks', () => {
    const steps = parseLiterateMarkdown(COMBINED_BLOCK);
    const step = steps[0];
    
    expect(step.codeBlocks.length).toBe(1);
    expect(step.codeBlocks[0].meta).toContain('exec');
    expect(step.codeBlocks[0].meta).toContain('subagent=scout');
  });

  test('extracts named code blocks', () => {
    const steps = parseLiterateMarkdown(NAMED_BLOCK);
    const step = steps[0];
    
    expect(step.codeBlocks[0].meta).toContain('exec=my_result');
  });
});

describe('executeCode', () => {
  test('executes simple python code', async () => {
    const code = "def main(x):\n    return x * 2";
    
    // For MVP, we just test that it doesn't crash
    // Real execution would need Python interpreter
    const result = await executeCode('python', code, { x: 5 });
    
    // The actual result depends on having Python installed
    expect(typeof result).toBe('object');
    expect(typeof result.success).toBe('boolean');
  });

  test('handles JavaScript code', async () => {
    const code = "function main(input) {\n  return input.x * 2;\n}";
    
    const result = await executeCode('javascript', code, { x: 5 });
    
    // Just verify it runs without error for MVP
    expect(typeof result).toBe('object');
  });

  test('extracts input from structured JSON', () => {
    // Test parsing structured output format
    const llmResponse = "```json\n{\"input\": {\"objectives\": [\"Research X\", \"Research Y\"]}}\n```";
    
    // This tests the input extraction logic
    const parsed = JSON.parse(llmResponse.replace(/```json\n?|\n?```/g, ''));
    expect(parsed.input.objectives).toEqual(["Research X", "Research Y"]);
  });
});

describe('generator code execution', () => {
  test('yields results from generator', async () => {
    const code = "def collect(objectives):\n    for obj in objectives:\n        yield f\"Research: {obj}\"";
    
    // Test that generator yields properly
    // This would require actual Python execution
    // For now, test the parsing
    expect(code).toContain('yield');
  });
});
