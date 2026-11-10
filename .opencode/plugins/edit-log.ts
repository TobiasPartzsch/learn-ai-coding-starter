import { appendFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { Plugin } from "@opencode/plugin";

const LOGGED_TOOLS = new Set(["edit", "write", "patch"]);

export default Plugin.define({
  id: "applymaxxing.edit-log",
  setup: async (ctx) => {
    const logPath = join(ctx.location.project.canonical, "logs/plugin-tools.log");

    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return;
      if (!LOGGED_TOOLS.has(event.tool)) return;

      await mkdir(dirname(logPath), { recursive: true });
      await appendFile(logPath, `${JSON.stringify({ tool: event.tool, status: event.status })}\n`);
    });
  },
});
