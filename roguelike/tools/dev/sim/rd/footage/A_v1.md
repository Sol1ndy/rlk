# A_v1 — footage log, v1.mp4 (39.8 s, 1080p60)

Analyst A. Times are video seconds; `t` = Minecraft ticks (20 t/s) from the start of the video; `+Nt` = ticks relative to the
first cue of the current attack. Scale: player character ~1.8 b; boss ~1.9 b (about the same height as Xingqiu); estimates
are +-30 %. Catalog ids (A-xx) refer to `A_catalog.md`.

Video type: a Korean pattern-guide compilation. Title captions name each pattern (quoted below). Parts are shown twice:
real time first, then a 2x slow-motion replay. Timings come only from the real-time parts (frame-similarity check,
`work/A/repeat.py`).

Segment map: 0-11 intro | 11.5-18.5 model showcase (still/slow) | 19.0-21.9 real | 21.9-28.2 slow replay of 19.0-21.6 |
28.2-31.1 real | 31.1-35.1 slow replay of 28.6-30.6 | 35.3-39.8 real.

Evidence: `work/A/cs/v1_2fps_01..05.jpg`, `work/A/sheets/v1_18.8_10fps.jpg`, `v1_27.9_10fps.jpg`, `v1_28.75_20fps.jpg`,
`v1_35.3_10fps.jpg`, `v1_37.7_10fps.jpg`, `work/A/fr/v1_rear_closeup.jpg`, crops in `frames/A/v1_*`.

| time (s) | t | event |
|---|---|---|
| 0.0-11.0 | 0-220 | Intro. The boss stands still in front of a huge violet/black swirling vortex, between two dark-red pillars, in a night arena with candles. Captions: "라이덴 쇼군", then "특이사항": 1) she uses a polearm and a sword, each with its own skills; 2) her attacks are flashy and fast; 3) no unfair patterns, but many and complex; 4) bait her defensive patterns. (crop `v1_00.50_intro_vortex.png`) |
| 11.5-15.5 | 230-310 | Still showcase, polearm and sword side by side: "라이덴 쇼군 패턴분석 – 무작위로 검 또는 창으로 시작합니다" (she starts at random with the sword or the polearm). Model reference (`v1_12.50_model_polearm_vs_sword.png`). |
| 16.0-18.5 | 320-370 | "검 – 몽상의 일심: 공속이 빠르고 공격을 피하기 까다롭습니다" (sword: fast attack speed, hard to dodge). Sword close-up (`v1_16.50_model_sword_closeup.png`). |
| 18.9-19.0 | 378-380 | Real-time fight. The boss (holding the POLEARM, see the replay frame at 21.9) stands about 3 b from the player. |
| **19.10** | 382 | **A-01 Weapon switch -> sword.** First cue: she raises the weapon vertically. Caption "무기 전환 – 검: 변신 바로 전 혹은 변신이 끝난 후 무기를 전환합니다 / 전방에 범위 공격을 하고 필드 전체에 일정 시간 계속해서 벼락을 내리칩니다" (switches weapon just before or just after the transformation; does an area attack in front, then lightning keeps striking the whole field for a while). |
| 19.20 | 384 (+2) | A thin dark vertical hoop (about 2.5 b tall) surrounds her. |
| 19.30-19.40 | 386-388 (+4..+6) | The hoop tips flat into a translucent violet disc or dome. Audio onset 19.25. |
| 19.50-19.80 | 390-396 (+8..+14) | A swirling violet vortex disc at her feet grows to a radius of about 4-5 b. Audio 19.51. This is the visible wind-up; it is not a separate floor decal. |
| 19.90 | 398 (+16) | Bolts start crackling. Audio 19.87. |
| **20.00-20.20** | 400-404 (+18..+22) | **HIT**: a huge dome burst with lightning, radius about 6 b, centred on her (slightly toward her front). The player is knocked down at 20.3. Audio 20.06. (crop `v1_20.05_sword_switch_blast.png`) |
| 20.3-20.6 | 406-412 | Residual sparks. From 20.7 she holds the sword (switch complete, about 10 t of recovery). |
| 21.2-21.6 | 424-432 | **A-02 field lightning marker**: a pale whitish translucent flat disc (radius about 2.5 b) lies on the floor under the player. No bolt is visible before the cut at 21.9. |
| 21.9-28.2 | — | Slow replay of 19.0-21.6 (ignored for timing). |
| 27.9-28.2 | 558-564 | Real time. The player is close behind or beside the boss, attacking. |
| **28.20-28.85** | 564-577 | **A-02**: a big pale-lavender translucent ground disc (radius about 2.5-3 b, slightly brighter rim) is centred where the player stood. It stays in place while the player dodges away at 28.29. (crop `v1_28.30_pale_strike_disc.png`) |
| **28.80-28.85** | 576-577 | **A-03 Rear check (sword, "뒤 견제: 넓은 범위로 뒤를 벱니다")**. Tell: a white-violet glowing orb at the boss's sword hand (charge). |
| 28.95-29.10 | 579-582 | A-02 resolves: a vertical violet lightning bolt drops into the pale disc. At 29.10 an impact burst plus a flat white shock ring (radius about 3 b). At 29.15-29.30 dark-violet crystal shards burst up at that spot. Audio 29.23. Disc-to-bolt is at least 0.75 s (15 t). |
| **29.35-29.45** | 587-589 (A-03 +11..+13) | A-03: a thin straight lightning beam runs from the boss out about 10-12 b, to her rear (it reaches the far bolt spot). |
| **29.50-29.70** | 590-594 (A-03 +14..+18) | **HIT**: a giant slanted violet crystal blade-wall erupts along the line, about 12 b long, about 1.5 b wide, about 2 b tall, with jagged spikes. Audio 29.87. Gone by about 30.1. (crop `v1_29.60_rear_check_crystal_wall.png`) |
| 30.36 | 607 | Audio tail. 31.1-35.1 is a slow replay. |
| 35.29 | 706 | **A-04 뇌명 (sword dash, LONG-range variant)**. Caption "뇌명: 빠르게 좌우를 베면서 돌진합니다 / 원거리 – 라이덴과 같은 방향으로 천천히 회피" (dashes while slashing left and right; at long range, dodge slowly in the same direction she moves). The boss is far away. |
| 35.40-35.50 | 708-710 (+0..+2) | She blinks or streaks in to about 5-6 b in front of the player (**A-19**). Audio 35.33 / 35.78. |
| 35.60-35.80 | 712-716 (+4..+8) | Draws the sword back to her hip in an iai stance (violet arc trail). |
| **36.00** | 720 (+12) | **TELL**: a bright white-violet star flash at her hip or hand. Audio 36.05. |
| 36.09 | 722 | A violet ring flash (about 1 b) at her chest. |
| 36.20-36.70 | 724-734 | Holds the stance; her body crackles from 36.5. |
| **36.79-36.90** | 736-738 (+28..+30) | **HIT 1**: a giant dark-violet horizontal crescent slash (about 6 b wide, sweeping arc) sweeps through the player area as she dashes. (crop `v1_36.85_raimei_dash_slash.png`) |
| **37.00** | 740 (+32) | **HIT 2**: a crossing slash in the other direction (X-shaped lightning crash). Audio 37.02. |
| 37.09-37.19 | 742-744 | A diagonal dark lightning streak marks her dash path. |
| 37.29-37.59 | 746-752 | She ends about 6-8 b past her start point. Recovery is about 6-8 t. Audio 37.60. |
| 37.7-39.4 | 754-788 | She stands idle holding the sword while the player hits her freely (no reaction). |
| 39.40-39.70 | 788-794 | She raises the sword with a white crescent trail (the start of the next action; it continues in v2 as a slow replay). |

Notes
- Arena (real fight): a flat, endless-looking teal floor with faint ripple patterns, no walls in view. The intro area (night, pillars, vortex) is only the entrance.
- No floor decal comes before A-01, A-03 or A-04. The only floor marker in v1 is the pale strike disc (A-02).
