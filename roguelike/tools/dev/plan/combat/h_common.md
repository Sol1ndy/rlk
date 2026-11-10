# 홍련 rebuild — common brief for lanes H1 / H1c / H2 / H2c / H3 (lead, 11-11)

Project: a Minecraft Java 26.3 roguelike datapack (Korean UI). Repo `/home/user/rlk`, datapack root `roguelike/`,
namespace `rlk`. `S` = `/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad`.

## Setup
`git -C /home/user/rlk fetch origin wip/combat && git -C /home/user/rlk worktree add -b wip/combat-<lane> $S/cb/wt_<lane> origin/wip/combat`
(if the branch already exists on origin — a restart — check it out instead and resume from `<lane>_progress.md`).
Work only in your worktree. Never touch `/home/user/rlk` itself, another lane's worktree, or the release branch.

## Read first (all in your worktree)
- `roguelike/README.md` chapter 0: 0-4 (build order), 0-5 (gates), 0-6 (the user's rules), 0-8 (tools), 0-9 (known failures).
- `roguelike/tools/dev/plan/combat/`: `decisions.md` (the user's words), `hr_brief.md` (the lead), **`hr_design.md` — your
  contract; its §8 (lead rulings) wins over the rest**, `video_notes.md` + `ref/*.jpg` (the user's reference video, look at
  the sheets for your part), `c_progress.md` / `b_progress.md` (the new combat as built).
- `roguelike/tools/dev/sim/hr/`: `PLAN.md`, `contract.md`, the suites and drawing tools of the 11-06 build.

## Rules (the user's; breaking one is a defect)
- Generated outputs are never edited by hand: change the generator and regenerate; two runs must be byte-identical.
- Vanilla sounds only. No tip text of any kind (the one exception already in the design: the instant-death banner). Her 25
  lines are verbatim (`api.LINES`), never edited. No floor decals. No elemental immunity.
- Telegraph: a quiet tell ≥ 12 t (≥ 20 t for big hits), chain hits ≥ 10 t apart, aims lock 6-8 t before the hit.
- Real-game traps: no negative literal in `scoreboard players add/remove`; no glyph-font inheritance; lowercase resource
  ids; nothing below the floor; no teleport into blocks; held props point the right way; one display card per projectile;
  `summon` does not take the execute rotation; nothing too small or too thin to see.
- Only vanilla 26.3 commands that the real server parses (loadcheck is the judge, not the simulator).

## Resource pack (not in git)
The 11-06 release pack is unpacked read-only at `$S/rp_base`. Work on your own copy: `cp -r $S/rp_base $S/rp_<lane>` and
pass it as `--resourcepack`. Everything you add to the pack must come out of a generator that is in git (a hand-made
source image goes into git under `roguelike/tools/` and the generator copies it): the container can be replaced at any
time and only git survives. List the pack files you add or change in your progress file.

## Gates before every push
Your lane's suites; the existing `tools/dev/sim/hr` suites that concern your part (say which fail only because another
lane's part is still missing); `python3 tools/check_mboss_pack.py` → 0; the real-server load
`RLK_DEV=$S bash <wt>/roguelike/tools/dev/loadcheck.sh <wt>/roguelike <tag>` → 0 errors (one server at a time; the lock
queues you); when the pack changed: `python3 -I tools/dev/rplint.py <rp>` → 0 and `python3 -I tools/dev/atlas_px.py <rp>`
≤ 13.2 M px. Look at your own work with the drawing tools (rendered sheets of clips, shots, effects) before you call it done.

## Saving work
Commit after each gated step and `git push -u origin wip/combat-<lane>` (retry network errors after 2 / 4 / 8 / 16 s).
Keep `roguelike/tools/dev/plan/combat/<lane>_progress.md` current (done / next / decisions / requests to other lanes /
pack files): a fresh agent must be able to resume from it. No pull request. Every commit message ends with exactly
```
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019wi9c7roqDDkFi2TvFWw6G
```
and names no model anywhere else.

## Working with the other lanes
File owners are in `hr_design.md` §8.3. Do not edit another lane's source file, with one exception: a marked throwaway
stand-in so your part builds (`// STAND-IN (<lane>): replaced at the merge`); at the merge the owner's file wins whole.
H1 pushes an additive **interface commit** (`H1 interface …`) to `origin/wip/combat-hr1` first; until it is there take
names and numbers from `hr_design.md`, then `git fetch origin wip/combat-hr1 && git merge` it. Fixes to the combat core
may land on `origin/wip/combat` while you work: before your final report merge `origin/wip/combat`, regenerate, rerun the
gates. If the design is wrong or impossible somewhere, do the nearest sound thing, and write the deviation and the reason
in your progress file and report — do not stop to ask.

## Housekeeping
`df -h /` must keep ≥ 2 GB free; delete your scratch files when done (keep the worktree and your pack copy).

## Final report
What is built (by design section), gate results with numbers, deviations from the design and why, requests to other
lanes, pack files added or changed, and a short list of what only a person in the game can check.
