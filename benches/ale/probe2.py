#!/usr/bin/env python3
"""Introspect CaseResult + overall_judge_result for feedback design."""
import time
import ale_bench

s = ale_bench.start(problem_id="ahc008", lite_version=True, num_workers=12,
                    run_visualization_server=False)
t = time.time()
code = "#include<bits/stdc++.h>\nint main(){int n;if(std::cin>>n)std::cout<<0<<std::endl;return 0;}"
r = s.public_eval(code, code_language="cpp23", reuse_containers=True)
print("eval(cached start):", "%.1fs" % (time.time() - t))
print("overall_absolute_score:", r.overall_absolute_score)
print("overall_judge_result:", r.overall_judge_result)

SKIP = set(dir(object)) | {
    "construct", "copy", "dict", "from_orm", "json", "model_computed_fields",
    "model_config", "model_construct", "model_copy", "model_dump", "model_dump_json",
    "model_extra", "model_fields", "model_fields_set", "model_json_schema",
    "model_parametrized_name", "model_post_init", "model_rebuild", "model_validate",
    "model_validate_json", "model_validate_strings", "parse_file", "parse_obj",
    "parse_raw", "schema", "schema_json", "update_forward_refs", "validate",
}
cr = r.case_results[0]
print("CaseResult fields:", [a for a in dir(cr) if not a.startswith("_") and a not in SKIP])
for a in ("seed", "absolute_score", "relative_score", "judge_result", "status",
          "execution_time", "error_str", "output_str"):
    if hasattr(cr, a):
        print("  CaseResult.%s = %s" % (a, str(getattr(cr, a))[:120]))
s.close()
