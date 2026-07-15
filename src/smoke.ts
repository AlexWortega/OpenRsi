/**
 * Phase-0 smoke test: prove the pi + OpenRouter path drives end-to-end headlessly,
 * including a custom tool call. No benchmark, no GPU — just the agent skeleton.
 *
 * Run:  node --env-file=.env dist/smoke.js
 */
import { Type } from "typebox";
import { createAgentSession, defineTool } from "@earendil-works/pi-coding-agent";
import { SessionManager } from "@earendil-works/pi-coding-agent";
import { assertKey, modelSlug, tierModel } from "./provider.js";

async function main() {
  assertKey();
  const slug = modelSlug("outer");
  console.log(`[smoke] model = openrouter:${slug}`);

  let pinged: string | null = null;
  const pingTool = defineTool({
    name: "ping",
    label: "ping",
    description: "Health-check tool. Call it exactly once with a short message to confirm tool routing works.",
    parameters: Type.Object({
      message: Type.String({ description: "any short string" }),
    }),
    async execute(_id, { message }) {
      pinged = message;
      return { content: [{ type: "text" as const, text: `pong: ${message}` }], details: undefined };
    },
  });

  const { session } = await createAgentSession({
    model: tierModel("outer"),
    thinkingLevel: "low",
    customTools: [pingTool],
    noTools: "builtin", // drop built-in read/bash/edit/write, keep the custom ping tool
    sessionManager: SessionManager.inMemory(process.cwd()),
  });

  const events: string[] = [];
  const unsub = session.subscribe((e) => {
    if (e.type === "tool_execution_start" || e.type === "tool_execution_end") {
      events.push(`${e.type}`);
    }
  });

  await session.prompt(
    "Call the `ping` tool once with message 'openrsi-alive', then reply with the single word DONE.",
  );
  await session.waitForIdle();
  unsub();

  const stats = session.getSessionStats() as any;
  console.log(`[smoke] tool events: ${events.join(", ") || "(none)"}`);
  console.log(`[smoke] ping received: ${JSON.stringify(pinged)}`);
  if (stats) {
    console.log(
      `[smoke] tokens in/out=${stats.tokens?.input}/${stats.tokens?.output} cost=$${stats.cost?.toFixed?.(4) ?? stats.cost}`,
    );
  }

  if (pinged !== "openrsi-alive") {
    console.error("[smoke] FAIL: ping tool was not called with the expected message.");
    process.exit(1);
  }
  console.log("[smoke] PASS: pi + OpenRouter + custom tool routing works.");
  process.exit(0);
}

main().catch((err) => {
  console.error("[smoke] ERROR:", err?.stack || err);
  process.exit(1);
});
