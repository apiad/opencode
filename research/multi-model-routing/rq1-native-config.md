# Native Multi-Model Configuration in Gemini CLI (v0.34.0)

This report investigates the native multi-model configuration capabilities of Gemini CLI version 0.34.0, focusing on configuration structures, dynamic switching mechanisms, fallback behaviors, and parameter handling.

## 1. Native Model Definition and Configuration

In Gemini CLI v0.34.0, multiple models are defined and managed within the `.gemini/settings.json` file (at the project or user level) using two primary structures: `customAliases` and `overrides`.

### Custom Model Aliases (`modelConfigs.customAliases`)
The `customAliases` object allows users to define named presets that can inherit from base models or other aliases. This is useful for creating specialized configurations for different tasks.

- **Inheritance (`extends`):** An alias can extend another alias or a base model.
- **Parameter Overrides:** Specific generation parameters (like temperature) can be set for each alias.

**Example Configuration:**
```json
{
  "modelConfigs": {
    "customAliases": {
      "research-pro": {
        "extends": "gemini-2.0-pro",
        "modelConfig": {
          "generateContentConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
          }
        }
      },
      "fast-exec": {
        "extends": "gemini-2.0-flash",
        "modelConfig": {
          "generateContentConfig": {
            "temperature": 0.1
          }
        }
      }
    }
  }
}
```

### Model Overrides (`modelConfigs.overrides`)
Overrides allow for context-aware model selection based on the "scope" or "agent" currently executing. This is part of the CLI's advanced routing system.

**Example Configuration:**
```json
{
  "modelConfigs": {
    "overrides": [
      {
        "match": { "overrideScope": "codebase_investigator" },
        "modelConfig": {
          "model": "gemini-2.0-pro",
          "generateContentConfig": { "temperature": 0 }
        }
      }
    ]
  }
}
```

### Intelligent Model Routing
The CLI includes a built-in "Plan Mode Routing" feature (enabled by `general.plan.modelRouting: true`) that automatically selects high-reasoning models (Pro) for planning and high-speed models (Flash) for implementation tasks.

## 2. Dynamic Model Switching: Flags and Environment Variables

Gemini CLI provides several mechanisms to override the default model or switch models dynamically during execution.

### Precedence Order (Highest to Lowest)
1. **Command-line flag:** `--model <model-name>` (or `-m`)
2. **Environment variable:** `GEMINI_MODEL`
3. **Project Settings:** `.gemini/settings.json` in the current directory.
4. **User Settings:** `~/.gemini/settings.json`.
5. **System Defaults:** Global configuration files or hardcoded defaults.
6. **Intelligent Router:** If set to `auto` (e.g., `auto-gemini-3`), the system chooses dynamically.

### CLI Flags
- `--model <name>`: Sets the model for the current command.
- `--no-model-fallback`: Disables the automatic fallback mechanism.

### Interactive Commands
Inside the CLI interactive mode, users can switch models using:
- `/model`: Opens a menu to select between **Auto**, **Pro**, **Flash**, or a manual entry.
- `/settings`: Allows toggling the "Model Router" and other configuration options.

## 3. Default Fallback Behavior

The CLI employs a `ModelAvailabilityService` to handle scenarios where a requested model is unavailable (e.g., due to quota limits or API errors).

### Interactive Fallback
In an interactive session, if the primary model fails, the CLI typically prompts the user to select an alternative model to continue the session.

### Silent Fallback Chain (Utility Calls)
For background tasks or internal utility calls (such as prompt completion or classification), the CLI uses a hardcoded silent fallback sequence:
1. `gemini-2.5-flash-lite` (Primary)
2. `gemini-2.5-flash` (Secondary)
3. `gemini-2.5-pro` (Final attempt)

### Disabling Fallback
Users can force the CLI to error out rather than falling back by setting:
- **Settings:** `"disableModelFallback": true`
- **CLI Flag:** `--no-model-fallback`

## 4. Handling of Model-Specific Parameters

When switching between models (either manually or via the router), model-specific parameters are managed through the `modelConfig` object.

### Parameter Merging
- **Inheritance Logic:** When an alias `extends` another, the child's `generateContentConfig` is merged with the parent's. The child's values overwrite the parent's for the same keys.
- **Switching Consistency:** When the CLI switches models (e.g., from Pro to Flash in Plan Mode), it applies the configuration associated with the target model or alias defined in the `modelConfigs`.

### Key Parameters Supported
The following parameters are typically handled within the `generateContentConfig` block during a switch:
- `temperature`
- `maxOutputTokens`
- `topP`
- `topK`
- `stopSequences`
- `responseMimeType`

This structured approach ensures that specialized models (like a "creative" alias) maintain their specific temperature settings even when the underlying base model is updated or switched.
