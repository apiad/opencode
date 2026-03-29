/**
 * Question & Routing tests
 */

import { describe, test, expect } from 'bun:test';
import { 
  parseLiterateMarkdown, 
  parseQuestionConfig,
  routeFromQuestion,
  shouldLoopStep,
  type Step
} from './literate-commands';

// ============================================================================
// Test Data
// ============================================================================

const QUESTION_STEP = `---
\`\`\`yaml {config}
step: approval
question:
    title: Do you approve the plan?
    options:
        Yes: collect
        No*: refine
\`\`\`
Please approve or refine.
`;

const LOOP_STEP = `---
\`\`\`yaml {config}
step: refine
next: approval
max-iter: 3
\`\`\`
Refine the plan based on feedback.
`;

const LINEAR_STEP = `---
\`\`\`yaml {config}
step: step1
next: step2
\`\`\`
Do step 1.
`;

const LINEAR_STEP_2 = `---
\`\`\`yaml {config}
step: step2
\`\`\`
Do step 2.
`;

// ============================================================================
// Tests
// ============================================================================

describe('parseQuestionConfig', () => {
  test('extracts question config from step', () => {
    const steps = parseLiterateMarkdown(QUESTION_STEP);
    const step = steps[0];
    
    const config = parseQuestionConfig(step.config);
    
    expect(config).toBeDefined();
    expect(config?.title).toBe('Do you approve the plan?');
    expect(config?.options).toEqual({
      'Yes': 'collect',
      'No*': 'refine'
    });
  });

  test('returns null for steps without question', () => {
    const steps = parseLiterateMarkdown(LINEAR_STEP);
    const step = steps[0];
    
    const config = parseQuestionConfig(step.config);
    
    expect(config).toBeNull();
  });
});

describe('routeFromQuestion', () => {
  test('routes based on Yes response', () => {
    const steps = parseLiterateMarkdown(QUESTION_STEP);
    const step = steps[0];
    
    const nextStep = routeFromQuestion(step.config, 'Yes');
    
    expect(nextStep).toBe('collect');
  });

  test('routes based on No response', () => {
    const steps = parseLiterateMarkdown(QUESTION_STEP);
    const step = steps[0];
    
    const nextStep = routeFromQuestion(step.config, 'No');
    
    expect(nextStep).toBe('refine');
  });

  test('returns null for unknown response', () => {
    const steps = parseLiterateMarkdown(QUESTION_STEP);
    const step = steps[0];
    
    const nextStep = routeFromQuestion(step.config, 'Maybe');
    
    expect(nextStep).toBeNull();
  });
});

describe('shouldLoopStep', () => {
  test('returns false for steps without max-iter', () => {
    const steps = parseLiterateMarkdown(QUESTION_STEP);
    const step = steps[0];
    
    const result = shouldLoopStep(step.config, 0);
    
    expect(result).toBe(false);
  });

  test('returns false when max-iter exceeded', () => {
    const steps = parseLiterateMarkdown(LOOP_STEP);
    const step = steps[0];
    
    // At iteration 3, should not loop (max is 3)
    const result = shouldLoopStep(step.config, 3);
    
    expect(result).toBe(false);
  });

  test('returns true when under max-iter', () => {
    const steps = parseLiterateMarkdown(LOOP_STEP);
    const step = steps[0];
    
    // At iteration 2, should loop
    const result = shouldLoopStep(step.config, 2);
    
    expect(result).toBe(true);
  });
});

describe('routing flow', () => {
  test('linear routing via next:', () => {
    const steps = parseLiterateMarkdown(LINEAR_STEP);
    const step1 = steps[0];
    
    expect(step1.config.next).toBe('step2');
  });

  test('routing integration - approval loop', () => {
    // Simulate approval → No → refine → approval → Yes → collect
    const approvalStep = { config: { 
      step: 'approval', 
      question: { 
        title: 'Approve?', 
        options: { 'Yes': 'collect', 'No*': 'refine' } 
      } 
    }};
    
    // User says No
    let next = routeFromQuestion(approvalStep.config, 'No');
    expect(next).toBe('refine');
    
    // After refine, next is approval (loop)
    const refineStep = { config: { step: 'refine', next: 'approval', maxIter: 3 }};
    expect(refineStep.config.next).toBe('approval');
    
    // Loop check
    expect(shouldLoopStep(refineStep.config, 0)).toBe(true);
    expect(shouldLoopStep(refineStep.config, 3)).toBe(false); // Max reached
  });
});
