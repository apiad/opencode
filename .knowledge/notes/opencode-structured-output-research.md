---
id: opencode-structured-output-research
created: 2026-03-29
modified: 2026-03-29
type: research
status: active
tags:
  - opencode
  - sdk
  - structured-output
  - json-schema
  - api
sources:
  - https://opencode.ai/docs/sdk/
  - https://github.com/anomalyco/opencode/issues/15226
  - https://github.com/anomalyco/opencode/issues/19700
  - https://github.com/anomalyco/opencode/issues/10456
---

# OpenCode Structured Output Research

## Summary

OpenCode supports structured JSON output via the `format` parameter in `session.prompt()`. The feature works by passing a JSON Schema to the model and using automatic retries for validation. However, there are **known compatibility issues** with certain model/provider combinations.

---

## 1. The `format` Parameter API

### Location
`client.session.prompt({ path: { id: sessionId }, body: { format: {...} } })`

### Parameters

| Field | Type | Description |
|-------|------|-------------|
| `type` | `"json_schema"` \| `"text"` | Output format type. `"text"` is default (no structured output) |
| `schema` | `object` | JSON Schema defining the output structure |
| `retryCount` | `number` | Number of validation retries (default: 2) |

### Basic Usage

```typescript
const result = await client.session.prompt({
  path: { id: sessionId },
  body: {
    parts: [{ type: "text", text: "Research Anthropic and provide company info" }],
    format: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          company: { type: "string", description: "Company name" },
          founded: { type: "number", description: "Year founded" },
          products: {
            type: "array",
            items: { type: "string" },
            description: "Main products",
          },
        },
        required: ["company", "founded"],
      },
    },
  },
})

// Access structured output
console.log(result.data.info.structured_output)
// { company: "Anthropic", founded: 2021, products: ["Claude", "Claude API"] }
```

---

## 2. Model/Provider Requirements

### What the Documentation Says
The documentation states that structured output uses a `StructuredOutput` tool internally, but **does not explicitly require specific models**.

### Key Models That Support It
Based on the documentation, models good at tool calling (recommended for OpenCode) include:
- GPT 5.2
- GPT 5.1 Codex
- Claude Opus 4.5
- Claude Sonnet 4.5
- Minimax M2.1
- Gemini 3 Pro

### Known Compatibility Issues

#### Issue #15226: Thinking Models Incompatibility (OPEN)
**Severity: HIGH**

- **Problem**: When using reasoning/thinking-enabled models (e.g., Kimi K2.5), OpenCode unconditionally sets `toolChoice: "required"` for the StructuredOutput tool
- **Error**: `"tool_choice 'required' is incompatible with thinking enabled"`
- **Affected**: Any model with `reasoning: true` accessed via providers that enforce this incompatibility
- **Status**: Open and unfixed as of v1.2.14

**Root Cause**:
```typescript
// In SessionPrompt.loop():
toolChoice: format4.type === "json_schema" ? "required" : undefined
// Plus separately:
result["thinking"] = { type: "enabled", budgetTokens: ... }
// Both sent together → provider rejects
```

#### Issue #19700: AI SDK v6 Breaking Vertex AI (CLOSED)
**Severity: MEDIUM (fixed)**

- **Problem**: AI SDK v6 (`@ai-sdk/anthropic@3.0.64`) sends unsupported `structured-outputs-2025-11-13` header to Vertex AI
- **Error**: `"Unexpected value(s) \`structured-outputs-2025-11-13\` for the \`anthropic-beta\` header"`
- **Affected**: opencode v1.3.4/v1.3.5 via Vertex AI
- **Status**: Closed (fixed)

---

## 3. What Happens When Structured Output Fails

### Automatic Retry
OpenCode automatically retries failed validations (default: 2 retries, configurable).

### Error Response
If all retries fail, the response includes a `StructuredOutputError`:

```typescript
if (result.data.info.error?.name === "StructuredOutputError") {
  console.error("Failed to produce structured output:", result.data.info.error.message)
  console.error("Attempts:", result.data.info.error.retries)
}
```

### Error Structure
```typescript
{
  error: {
    name: "StructuredOutputError",
    message: string,
    retries: number
  }
}
```

---

## 4. Community Issues & Discussions

### Closed Issues
| Issue | Status | Description |
|-------|--------|-------------|
| #10456 | Closed (implemented) | Feature request for JSON Schema structured output - **IMPLEMENTED** |
| #19700 | Closed (fixed) | AI SDK v6 breaking Vertex AI - **FIXED** |

### Open Issues
| Issue | Status | Description |
|-------|--------|-------------|
| #15226 | Open | Thinking models incompatible with `toolChoice: "required"` |

### Feature History
- **#10456** was the original feature request (Jan 2026)
- It was **implemented** via PR #17276, adding `format.type: "json_schema"` support
- The feature uses a `StructuredOutput` tool internally

---

## 5. Alternative Approaches for Reliable Structured Data

### Option A: Use Non-Thinking Models
If you need guaranteed structured output, use models **without** thinking/reasoning enabled:
- Claude Sonnet 4.5 (non-thinking variant)
- GPT 4o
- Gemini 3 Flash

### Option B: Use OpenCode Zen
According to issue #15226, OpenCode Zen "reconciles the conflict server-side" while OpenCode Go does not.

```typescript
model: { providerID: "opencode", modelID: "claude-opus-4-6" }
// vs
model: { providerID: "opencode-go", modelID: "kimi-k2.5" }
```

### Option C: Prompt Engineering
Include schema in the prompt and parse the response:
```typescript
const result = await client.session.prompt({
  body: {
    parts: [{
      type: "text",
      text: `Return valid JSON matching this schema:
      {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}
      Respond ONLY with JSON, no markdown fences.`
    }]
  }
})
// Parse result.data.info.text or similar
```

### Option D: Post-Processing with Validation
```typescript
import Ajv from "ajv"

const ajv = new Ajv()
const validate = ajv.compile(schema)

if (!validate(result.data.info.structured_output)) {
  // Retry with feedback
  await client.session.prompt({
    body: {
      parts: [{
        type: "text",
        text: `Previous output was invalid. Errors: ${JSON.stringify(validate.errors)}.
        Please correct and return only valid JSON.`
      }]
    }
  })
}
```

### Option E: Direct AI SDK Usage
For guaranteed structured output, bypass OpenCode and use the AI SDK directly:
```typescript
import { generateText } from "ai"

const { object } = await generateText({
  model: myModel,
  prompt: "...",
  schema: MySchema,
  provider: "openai" // or anthropic, etc.
})
```

---

## Recommendations

### For Maximum Reliability

1. **Use OpenCode Zen provider** if available (handles edge cases server-side)
2. **Use non-reasoning models** (avoid thinking-enabled models)
3. **Set higher retryCount** for complex schemas:
   ```typescript
   format: {
     type: "json_schema",
     schema: complexSchema,
     retryCount: 5
   }
   ```
4. **Provide clear property descriptions** in your JSON Schema
5. **Keep schemas simple** - avoid deeply nested complex schemas
6. **Handle errors gracefully** with the `StructuredOutputError` check

### Quick Start Working Example

```typescript
import { createOpencode } from "@opencode-ai/sdk"

const { client } = await createOpencode()
const session = await client.session.create({ body: { title: "Structured Test" } })

const result = await client.session.prompt({
  path: { id: session.id },
  body: {
    model: { providerID: "opencode", modelID: "claude-sonnet-4-5" }, // Non-thinking
    parts: [{ type: "text", text: "Analyze this code and return metrics" }],
    format: {
      type: "json_schema",
      schema: {
        type: "object",
        properties: {
          linesOfCode: { type: "number" },
          functions: { type: "number" },
          complexity: { type: "string", enum: ["low", "medium", "high"] }
        },
        required: ["linesOfCode", "functions", "complexity"]
      },
      retryCount: 3
    }
  }
})

if (result.data.info.structured_output) {
  console.log("Success:", result.data.info.structured_output)
} else if (result.data.info.error?.name === "StructuredOutputError") {
  console.error("Failed after retries:", result.data.info.error.message)
}
```

---

## Conclusion

**Structured output works** but has known limitations:

✅ **Works well with:**
- Non-reasoning models
- OpenCode Zen provider
- Simple to medium complexity schemas

⚠️ **Known issues:**
- Thinking-enabled models may fail (Issue #15226 - open)
- Some provider combinations have compatibility issues

**Best practice:** Test with your specific model/provider combination and implement fallback logic.
