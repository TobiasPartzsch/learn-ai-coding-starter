# Parser conventions

- Use one method per grammar rule (for example `expression`, `term`, `factor`, `call`, `primary`). Do not inline a rule's parsing into its caller.
- Make syntax errors describe what token was found. Use the existing `expect`/`error` helpers so diagnostics end with `, found '<lexeme>'` or `, but reached end of file`.
