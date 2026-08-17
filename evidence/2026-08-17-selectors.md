# Live selector revalidation — 2026-08-17

Each row: `gjc -p --no-session --no-tools --model <selector> "Reply OK"`.

| selector | expect | result |
| --- | --- | --- |
| `anthropic/claude-opus-5:high` | ok | ok |
| `anthropic/claude-opus-5:medium` | ok | ok |
| `anthropic/claude-opus-4-8:high` | ok | ok |
| `anthropic/claude-sonnet-4-6:high` | ok | ok |
| `anthropic/claude-fable-5:high` | ok | ok |
| `anthropic/claude-fable-5:xhigh` | ok | ok |
| `anthropic/claude-sonnet-5:high` | ok | ok |
| `openai-codex/gpt-5.6-sol:high` | ok | ok |
| `openai-codex/gpt-5.6-sol:xhigh` | ok | ok |
| `openai-codex/gpt-5.6-terra:high` | ok | ok |
| `openai-codex/gpt-5.6-luna:high` | ok | ok |
| `openai-codex/gpt-5.5:high` | ok | ok |
| `openai-codex/gpt-5.4:high` | ok | ok |
| `google-antigravity/gemini-3.1-pro-low` | ok | ok |
| `google-antigravity/gemini-3.1-pro-low:high` | ok | ok |
| `google-antigravity/gemini-3-flash:low` | ok | ok |
| `openai-codex/gpt-5.6-terra:medium` | ok | ok |
| `openai-codex/gpt-5.6-luna:medium` | ok | ok |
| `xai/grok-4.6:medium` | ok | ok |
| `xai/grok-4.6:high` | ok | ok |
| `xai/grok-4.5:medium` | ok | ok |
| `xai/grok-4.5:high` | ok | ok |
| `xai/grok-4.3:high` | ok | ok |
| `xai/grok-4-fast:high` | ok | ok |
| `opencode-go/glm-5.2` | ok | ok |
| `xai/grok-4-1-fast:high` | ok-live | ok |
| `opencode-go/deepseek-v4-flash` | ok-live | fail[] |
| `opencode-go/deepseek-v4-pro` | ok-live | fail[] |
| `grok-build/grok-4.6` | ok-live | ok |
| `google-antigravity/gemini-3.5-flash-low` | ok-live | ok |
| `google-antigravity/gemini-3.5-flash` | fail | fail[] |
| `google-antigravity/gemini-3.1-pro-high` | fail | fail[] |
| `google-antigravity/gemini-3.1-pro-bogus` | fail | fail[] |
| `openai-codex/gpt-5.3-codex:high` | fail | fail[not supported] |
| `xai/grok-4.6:bogus` | fail | fail[] |
| `openai-codex/gpt-5.6-sol:bogus` | fail | fail[] |
| `grok-build/grok-4.6:high` | fail | fail[] |

## Single-message @file input limit (separate from the 1M context window)

needle answer = ZULU555

| selector | @tokens | result |
| --- | --- | --- |
| `anthropic/claude-opus-5:high` | 350k | found |
| `anthropic/claude-opus-5:high` | 476k | found |
| `xai/grok-4-fast:high` | 476k | found |
