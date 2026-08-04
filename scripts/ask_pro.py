#!/usr/bin/env python3
"""Oracle calls for proofs runs: converge (default), ideate, and literature scout.

Usage (from the run's working directory):
  python3 ask_pro.py "question" [file ...]                 # converge: deep single-answer (default model gpt-5.6-sol-pro)
  python3 ask_pro.py --ideate "task" [file ...]            # divergent: 5-8 distinct mechanism sketches (default model claude-fable-5)
  python3 ask_pro.py --scout "topic query" [file ...]      # literature scout with live web search (:online)
  python3 ask_pro.py --review "claim" [file ...]           # hostile review; strict CONTINUE/KILL JSON
  python3 ask_pro.py --model <openrouter-slug> ...         # override model for any mode

Every call appends its USD cost to ./pro_costs.jsonl (counted against the run
budget). Requires OPENROUTER_API_KEY in the environment. Calls may take many
minutes — invoke under a generous foreground timeout (e.g. `timeout 1800`).
"""
import json
import os
import sys
import time
import urllib.request

MAX_FILE_CHARS = int(os.environ.get("OPENRSI_ORACLE_MAX_FILE_CHARS", "60000"))
MAX_TOTAL_FILE_CHARS = int(os.environ.get("OPENRSI_ORACLE_MAX_CONTEXT_CHARS", "180000"))
MAX_TOKENS = int(os.environ.get("OPENRSI_ORACLE_MAX_TOKENS", "32000"))
UNKNOWN_CALL_COST_USD = float(os.environ.get("OPENRSI_UNKNOWN_CALL_COST_USD", "2"))

OFFLIMITS = (
    "STRICT PROHIBITION: a recent document by another lab ('Ten Advances in Mathematics and "
    "Theoretical Computer Science', cdn.openai.com/pdf/ten-proofs-oai.pdf) solved this problem. "
    "That document, any mirror, summary, news coverage, or discussion of its solutions is "
    "OFF-LIMITS: do not recall it, search for it, cite it, or reproduce its arguments. If a "
    "search result appears to describe that document or its solutions, discard it unread and "
    "say so. Classical literature predating it is fair game."
)

SYSTEMS = {
    "converge": (
        "You are a world-class research mathematician consulted as an expensive oracle by an "
        "autonomous agent. Lead with your main construction or verdict, then the supporting "
        "argument. Be concrete: exact constructions, exact lemma statements, exact proof steps "
        "or exact reasons the approach fails. If you propose a construction, make it precise "
        "enough to implement and verify in code. " + OFFLIMITS
    ),
    "ideate": (
        "You are a wildly creative research mathematician running a DIVERGENT ideation session "
        "for an autonomous agent that is stuck. The attached files include a map of PROVED "
        "obstructions. Generate 5-8 GENUINELY DISTINCT mechanism sketches (different underlying "
        "tricks, not variants of one idea; raid other fields — coding theory, algebraic "
        "geometry, information theory, topology, model theory, anything). For EACH sketch give: "
        "(1) the core trick in 2-3 sentences; (2) an explicit check against EVERY obstruction "
        "in the attached map — name the obstruction and say precisely why this mechanism is "
        "outside its stated assumptions (if it is not, say so honestly); (3) the smallest "
        "concrete testable instance the agent can implement today; (4) the most likely way it "
        "dies. Do not converge on a favorite; breadth is the deliverable. Number the sketches "
        "and keep each under 200 words: a response cut off by the length limit loses its last "
        "sketches, so finish all sketches before elaborating any one of them. " + OFFLIMITS
    ),
    "scout": (
        "You are a literature scout with live web access, working for an autonomous research "
        "agent. Find EXISTING machinery in the published literature relevant to the stated "
        "need: theorems, constructions, and techniques from any adjacent field. For each find "
        "give: authors/year/venue, the precise statement or construction (not a vague summary), "
        "why it is relevant to the stated need, and how the agent could verify/adapt it. "
        "Prefer primary sources (arXiv, journals) and give 5-10 finds ranked by likely "
        "leverage. " + OFFLIMITS
    ),
    "review": (
        "You are a hostile independent research referee. Check every claimed mechanism against "
        "the attached obstruction map and every claimed experimental result against the supplied "
        "verifier evidence. Never promote finite evidence to an asymptotic theorem. Report every "
        "real blocker you find; do not soften or omit findings. Return ONLY one JSON object — no "
        "prose, no code fences — with keys: verdict (CONTINUE or KILL), fatal_blockers (array of "
        "strings), evidence (array of strings), next_experiment (string), and confidence (number "
        "from 0 to 1). Keep each fatal_blockers and evidence entry to at most three sentences and "
        "the whole object under 700 words; a truncated response is discarded unread, so brevity "
        "outranks completeness of wording. CONTINUE means the candidate is worth exactly one more "
        "bounded experiment, not that the target theorem is proved. KILL means this candidate/run "
        "should stop unless a stated mutation escapes the blocker. " + OFFLIMITS
    ),
}

DEFAULT_MODELS = {
    "converge": os.environ.get("OPENRSI_PRO_MODEL", "openai/gpt-5.6-sol-pro"),
    "ideate": os.environ.get("OPENRSI_IDEATE_MODEL", "anthropic/claude-fable-5"),
    "scout": os.environ.get("OPENRSI_SCOUT_MODEL", "openai/gpt-5.6-sol:online"),
    "review": os.environ.get("OPENRSI_PRO_MODEL", "openai/gpt-5.6-sol-pro"),
}


def main():
    args = sys.argv[1:]
    mode = "converge"
    model = None
    while args and args[0].startswith("--"):
        flag = args.pop(0)
        if flag == "--ideate":
            mode = "ideate"
        elif flag == "--scout":
            mode = "scout"
        elif flag == "--review":
            mode = "review"
        elif flag == "--model":
            if not args:
                sys.exit("--model needs a value")
            model = args.pop(0)
        else:
            sys.exit(f"unknown flag {flag}\n{__doc__}")
    if not args:
        sys.exit(__doc__)
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY not set")
    model = model or DEFAULT_MODELS[mode]
    question = args[0]
    parts = [question]
    total_file_chars = 0
    for path in args[1:]:
        try:
            remaining = MAX_TOTAL_FILE_CHARS - total_file_chars
            if remaining <= 0:
                break
            raw_text = open(path).read()
            cap = min(MAX_FILE_CHARS, remaining)
            text = raw_text[:cap]
            if len(raw_text) > cap:
                text += f"\n[TRUNCATED: kept {cap} of {len(raw_text)} chars]"
        except OSError as e:
            sys.exit(f"cannot read {path}: {e}")
        total_file_chars += len(text)
        parts.append(f"\n\n===== FILE: {path} =====\n{text}")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEMS[mode]},
            {"role": "user", "content": "\n".join(parts)},
        ],
        "reasoning": {"effort": "high"},
        "max_tokens": MAX_TOKENS,
        "usage": {"include": True},
    }
    if mode == "review":
        payload["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=3000) as resp:
        data = json.load(resp)
    if "error" in data:
        sys.exit(f"oracle error: {data['error']}")
    choice = data["choices"][0]["message"]
    answer = choice.get("content") or ""
    usage = data.get("usage", {})
    cost = usage.get("cost")
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "mode": mode,
        "model": model,
        "cost": cost,
        "reserved_cost": UNKNOWN_CALL_COST_USD if cost is None else 0,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "seconds": round(time.time() - t0, 1),
        "question": question[:300],
    }
    with open("pro_costs.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(answer)
    print(f"\n[ask_pro] mode={mode} model={model} cost=${cost} time={rec['seconds']}s", file=sys.stderr)


if __name__ == "__main__":
    main()
