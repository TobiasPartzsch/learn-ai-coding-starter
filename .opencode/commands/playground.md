---
description: Start the Sloperator playground server on a chosen port
---

Start the Sloperator playground server.

Requested port: $ARGUMENTS

If the requested port above is empty, use 8080.

Current TCP listeners:

!`lsof -nP -iTCP -sTCP:LISTEN`

Before starting anything, check the listener output above and verify with `pgrep -af playground/server.py` whether a Sloperator playground server is already running. If one is listening, do not start a second instance; report its PID, port, and URL instead.

Otherwise start the server in the background from the project root with:

uv run playground/server.py <port>

Replace `<port>` with the requested port, or 8080 when the argument was empty. Do not block the session on the server. Report the URL, the PID, and how to stop it.
