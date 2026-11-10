import { appendFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { Plugin } from "@opencode/plugin";

export default Plugin.define({
  id: "applymaxxing.playground-log",
  setup: async (ctx) => {
    const logPath = join(ctx.location.project.canonical, "logs/plugin-playground.log");

    await ctx.tool.hook("execute.before", async (event) => {
      if (event.tool !== "shell") return;

      const { command } = event.input as { command?: unknown };
      if (typeof command !== "string" || !command.includes("playground/server.py")) return;

      await mkdir(dirname(logPath), { recursive: true });
      await appendFile(logPath, "playground shell request\n");
    });
  },
});
