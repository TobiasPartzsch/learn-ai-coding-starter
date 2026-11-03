import { execFile } from "node:child_process";
import { Plugin } from "@opencode/plugin";

interface SlopResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function runSloperator(file: string, projectRoot: string): Promise<SlopResult> {
  return new Promise((settle, fail) => {
    execFile(
      "uv",
      ["run", "--no-active", "sloperator.py", file],
      { cwd: projectRoot, maxBuffer: 10 * 1024 * 1024 },
      (error, stdout, stderr) => {
        // A string code means the process never started (e.g. uv is not installed).
        if (error && typeof error.code === "string") {
          fail(error);
          return;
        }

        if (error?.signal) {
          stderr += `${stderr === "" || stderr.endsWith("\n") ? "" : "\n"}terminated by signal ${error.signal}`;
        }

        settle({
          stdout,
          stderr,
          exitCode: error ? (typeof error.code === "number" ? error.code : -1) : 0,
        });
      },
    );
  });
}

export default Plugin.define({
  id: "applymaxxing.run-slop",
  setup: async (ctx) => {
    const projectRoot = ctx.location.project.canonical;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) file with Sloperator and return stdout, stderr, and exitCode as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, relative to the project root or absolute.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const result = await runSloperator(path, projectRoot);
          return { content: JSON.stringify(result, null, 2) };
        },
      });
    });
  },
});
