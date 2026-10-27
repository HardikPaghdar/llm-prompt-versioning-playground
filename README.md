# LLM Prompt Versioning Playground

A local prompt registry built on SQLite, with immutable named versions, SHA-256 fingerprints, history lookup, and a helper for comparing recorded evaluation fixtures.

## Features
- Save prompt versions without overwriting earlier text.
- Retrieve the latest or a specific version and inspect history.
- Track a content hash for reproducibility.
- Compare before/after fixture records to highlight changed cases.

## Quick start
Requires Python 3.10+; SQLite ships with Python.

```bash
python - <<'PY'
from app import PromptRegistry
registry = PromptRegistry("local-prompts.db")
print(registry.save("support-answer", "Use only the supplied policy."))
print(registry.save("support-answer", "Use only the supplied policy; say when it is insufficient."))
print(registry.history("support-answer"))
PY
```

## Tests
`python -m unittest discover -s tests -v`

## Limitations
This project does not call an LLM or execute prompts. Fixture comparison evaluates saved records, not semantic correctness. The local SQLite database can contain sensitive prompt content; keep it out of source control and production logs. Add access control, migrations, provider-specific run adapters, and reviewed evaluation datasets before team deployment.
