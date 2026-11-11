import { execFile } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join } from "node:path";
import { Plugin } from "@opencode/plugin";

interface SlopResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

interface ExampleOutput {
  name: string;
  exitCode: number;
  firstLine: string;
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

function firstLine(stdout: string): string {
  return stdout.split(/\r?\n/, 1)[0];
}

export default Plugin.define({
  id: "applymaxxing.example-outputs",
  setup: async (ctx) => {
    const projectRoot = ctx.location.project.canonical;
    const examplesDir = join(projectRoot, "examples");

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every SlopLang (.slop) file in examples/ and return each file's exit code and first output line as JSON.",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const entries = await readdir(examplesDir, { withFileTypes: true });
          const files = entries
            .filter((entry) => entry.isFile() && entry.name.endsWith(".slop"))
            .map((entry) => entry.name)
            .sort();

          const examples: ExampleOutput[] = await Promise.all(
            files.map(async (name) => {
              const result = await runSloperator(join(examplesDir, name), projectRoot);
              return {
                name,
                exitCode: result.exitCode,
                firstLine: firstLine(result.stdout),
              };
            }),
          );

          return { content: JSON.stringify({ examples }, null, 2) };
        },
      });
    });
  },
});
