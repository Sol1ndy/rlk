# Round V, lane VI (the integration of lanes VC / VP / VB) — progress

Branch `wip/v-int` (from `origin/wip/v` 2793b54cd), worktree `<S>/cb/wt_vi`, pack `<S>/rp_vi` (from `<S>/rp_fin`, the 11-11b
release pack); scratch `<S>/cb/vi` (deleted at the end). Contract: `v_brief.md`, the three lanes' progress files
(`vc_progress.md`, `vp_progress.md`, `vb_progress.md`). Work in progress: this file is rewritten at the end.

## Steps
- [x] merges: `wip/v-cam` 303407e78, `wip/v-player` 477b8977a, `wip/v-boss` 252f88ca3 then its final head 1163bba57
- [x] full regeneration (README 0-4 order) twice: the merged tree is its own fixed point
- [x] the cross-lane requests (below)
- [x] `tests/test_vi.py` (the seams: beatpat / follow / swap / beatseq / skip)
- [ ] hrfair 2.0 on the final tree, gates, docs, the pack's README
