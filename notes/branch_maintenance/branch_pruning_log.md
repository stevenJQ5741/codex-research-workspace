# Branch Pruning Log

## 2026-08-04 - Dry run

### Repository state

- default branch: `agent/20260727-1245-presentation-workflow`
- previous default: `agent/20260716-1402-main`
- open pull requests: 0
- remote branches: 3
- remote tags before this cycle: 0
- planned local annotated snapshot: `snapshot/2026-H1`
- snapshot target: `0555b5a223cc84f697b6f3fc8d70e669a205f734`
  (`2026-06-29T11:13:29+09:00`)
- age cutoff: branch tip earlier than `2026-02-04T00:00:00+09:00`

Branch-tip commit time is authoritative for age. Branch-name time is supporting
evidence only.

### Dry-run table

| Remote branch | Tip commit | Tip time (JST) | Older than 6 months | Open PR | Active/protected reason | Unique commits vs current default | Covered by current default or snapshot | Delete candidate |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| `agent/20260727-1245-presentation-workflow` | `01bee94` | 2026-07-27 13:06 | no | no | current default and active work | 0 | yes | no |
| `agent/20260716-1402-main` | `b326172` | 2026-07-16 14:02 | no | no | previous default | 0 | yes | no |
| `agent/20260716-1401-integrate-research-skills` | `2137450` | 2026-07-16 13:27 | no | no | age criterion not met | 0 | yes | no |

### Decision

No remote branch satisfies all deletion criteria. No remote deletion is proposed
or authorized. All three branch tips are reachable from the current default.

### Post-cycle checks

- [x] local annotated `snapshot/2026-H1` created at the recorded target
- [x] local tag resolves to the expected commit
- [x] no remote tag pushed without approval
- [x] default branch unchanged
- [x] `origin/HEAD` unchanged
- [x] protected branch reachability unchanged
