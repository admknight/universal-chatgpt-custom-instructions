# Release Qualification

- Version: `1.0.4`
- Validation tier: `SCENARIO_PASS`
- Release state: `SCENARIO_VALIDATED`
- Runtime dependency: `USER_UI_DEPENDENT`
- Revised-block live runtime validation: `NOT_RUN`
- Production-ready claim: **NO**

A fresh live personal v1.0.3 Custom Instructions RFQ test exposed a residual MAJOR scope-control defect in the shared logic: punching was still promoted into an explicit RFQ decision (specify unpunched or provide punching details) because it could affect price, despite no project basis. v1.0.4 makes the trigger gate explicit: common practice/options, usefulness, risk or price impact alone are not basis; absence is not ambiguity; without basis, omit rather than choosing an option. Structural, character-budget, source-hierarchy, preservation and expanded deterministic scenario/regression checks pass for both public variants. The revised v1.0.4 public blocks still require a live intended-runtime pilot before `RUNTIME_PASS` or `PRODUCTION_READY`.
