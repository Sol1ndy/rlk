# Review B (enemy side) — lead rulings (11-11). Findings and the per-boss table: `findings_B.json`. Fix lane: `wip/combat-fix-b`.

The user's decision this serves: 「패링 불가 공격: 보스의 일부 큰 공격만(범위 공격 · 잡기 등), 원작처럼 색 섬광으로 미리 보여 줌(글자 안내 없이)」.

| id | ruling |
|---|---|
| B-01 | Adopt the reviewer's rule. **Default (`mboss/hz/np_def`)**: unparriable only for no-dodge hazards, per-mille hits, full-arena and mask hazards, and re-arming (lingering) hazards. Everything else — lanes, sectors, discs, rings of any size, every projectile — is parryable unless the module says `noparry=1`. **Per-module `noparry=1` list** (the biggest quarter): 파수꾼 P5 하늘을 심판하는 자 + 파괴 실패 창; 나비 달빛 해제; 역장 C5 지면 충격; 야타용왕 서리 · B3 emerge · 운석의 큰 원; 아펩 P1 꼬리 · 글로우(discs) · 시듦; 타키 착지 원(11); 아를레키노 Q4 빔 · Q5a · Q5b 마무리 · Q6 착지의 구체 원. One strike has one answer (no parryable + unparriable parts of the same hit). 나루카미: unchanged apart from B-11. 홍련: lane H's own list. |
| B-02, B-03 | The glint is drawn when the attack's visible tell starts — **≥ 12 t before the strike, and ≥ 20 t where the pattern's existing tell allows it** — at a rig locator (chest / head height on the visible body), never at the hit-box husk and never under the floor. Modules whose hazards are made at the strike frame call the glint from the pattern's tell tick. Do not change a boss's attack timing in this pass unless its unparriable hit would otherwise be announced < 12 t before; report the lead per attack. |
| B-04 | **The glint means "this cannot be parried: dodge it".** No-dodge attacks (jump the ring, stand in the safe circle, position only) and lingering fields / beams draw **no glint**: they keep their own tells. README 3's sentence follows. |
| B-05 | Fix (the groggy starts at the enemy). — lane `wip/combat-fix-a` (player/def). |
| B-06 | Fix (the archer's arrow carries its owner: a perfect parry takes the archer's pip). |
| B-07 | Fix: a perfect-parried cicin ram takes a pip from its owner caster; while the caster is groggy her cicins start no new ram. |
| B-08 | Fix (she is put on the floor). |
| B-09 | Fix (no pips from a boss that is not in play). |
| B-10 + A-04 | **One volley / one swing = one answer.** A perfect parry and a perfect dodge both consume the volley group (`grp_mark`), as a landed hit and a tier-1 / tier-2 parry already do; i-frames and a loose dodge do not. Swings made of per-tick wedges are one group per swing. README 3 and the suites that pin the rule follow. |
| B-11 | Follows from B-04: kind 9 (lingering) and kind 10 (the safe dome, no-dodge) draw no glint; nothing else changes. |
| B-12 | Fix the README lines (the 홍련 section is lane H's). |
| 아를레키노 Q5b | The nine cuts become parryable (F every 3 t works with the chain lock); the 30 % finisher stays unparriable with the glint ≥ 20 t before. Keep the damage a player takes when doing nothing as it is today. |
