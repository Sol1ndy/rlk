# v6.mp4 + w1.mp4 + w2.mp4 — frame-accurate breakdown — 아펩의 오아시스 파수꾼, phase 3 (기원 오아시스의 파수꾼), 종말의 여파, phase 2→3 cut-scene

Sources (all read-only): `src/v6.mp4` (1920x1080, 60 fps, 941 frames, AAC 48 kHz, 15.68 s, capture 03:14:42, the last
screen-recording clip), `src/w1.mp4` (500x300, 25 fps, 406 frames, 16.24 s, **no audio track**, wiki animation of
종말의 여파), `src/w2.mp4` (600x320, 25 fps, 488 frames, 19.52 s, **no audio track**, wiki animation of the phase 2→3
cut-scene).
Notation: `s` = seconds; `fNNNN` = source frame index (**60 fps for v6, 25 fps for w1/w2**); `tNNN` = Minecraft tick at 20 tps
(t = s·20); "X+n t" = ticks after event X. Images are in `understand/v6w/` (paths below are relative to it):
`keys/k_v6_fNNNN_*.jpg` (1280 px), `keys/k_w1_*`, `keys/k_w2_*` (native size), contact sheets `sheet*` (time / source frame /
tick printed on every cell: `sheet4fps_*` overviews, `sheet10fps_*` / `sheet20fps_*` / `sheet_perframe*` around actions, `sheet8fps_w*`
every 3rd frame of the wiki clips), zoom crops `zoom/zoom_fNNNN_*.jpg` (exact frame, header with time/frame/tick and crop box),
measuring grids `measure/grid_*.jpg` (full-frame pixel coordinates), 23 full-res PNGs in `full/`, HUD crops `hud_*`, spectrograms
`spec_*.png`, `speech_*.png`. Numeric logs: `cuts_v6.txt` / `cuts_w1.txt` / `cuts_w2.txt` + `framediff_*.npy`, `captions_metrics.txt`,
`bars.txt` (boss/player bar fill per frame), `w1_banner_metrics.txt`, `events.txt`, `bands_onsets.txt`, `onsets.txt`, `pal_*.txt`,
`pts_*.txt`, `measure/sizefit_f0480.txt`, `match_take3_vs_earlier.txt`.
Tools: `understand/v6w_tools/` (template tools from `mb3/understand/v1_tools` + the v4 neighbour's; new or rewritten: `csheet.py`
(contact sheets from a per-frame JPEG cache, any fps/size), `cuts.py` (fps argument), `keys.py` (3 key lists), `zoom.py`, `bars.py`,
`brightpal.py` (palette of glow pixels only), `sizefit.py` (pinhole ground-plane fit to the player, sizes vs camera height),
`events.py` windows rewritten for v6). The frame caches were deleted after use to save disk; rebuild with
`ffmpeg -i src/v6.mp4 -vf scale=640:360 -q:v 4 -start_number 0 v6w/cache_v6/%04d.jpg` and
`ffmpeg -i src/w1.mp4 -q:v 2 -start_number 0 v6w/cache_w1/%04d.jpg` (same for w2).
v6 is a screen recording of a YouTube guide: 12–40 % duplicate frames per second (capture judder), so v6 times are ±1 frame
(±0.02 s, ±0.3 t). **v6 audio trails the picture by ≈ 0.25–0.35 s** (impact sounds vs flashes); sound times below are audio times.
The wiki clips are native 25 fps: ±0.04 s (±0.8 t).

## 0. What these clips are (read this first)

* **v6 = the end of the uploader's phase-3 pattern guide** (same YouTube video as v1–v5: party 방랑자 / 미카 / **바바라 (active, Lv.90,
  21200 HP)** / 행추, UID 846551542, vertical watermark "흐구구구구" at the right edge). Every boss frame shows the nameplate
  **기원 오아시스의 파수꾼** / subtitle **「불씨」를 받아 소생한 생명**, Lv.90 (`hud_nameplates_t1_t2_t3.jpg`). **No phase 1, no phase 2
  organisms, no Heart progress bar, no death in v6.**
* **w1** = 종말의 여파 seen from start to end in one continuous take (phase 3, player = **나히다**, a short model ≈ 1.2–1.3 m — keep that
  in mind when using her as a ruler). **w2** = the in-engine phase 2→3 cut-scene (golden egg → ember → egg turns green → arena →
  emergence of the Warden of Oasis Prime), 5 shots, no text.
* **Edits in v6** (`cuts_v6.txt`, `cuts_check_1.55-1.75.jpg`, `cuts_check_8.6-9.2.jpg`, `cuts_check_14.4-14.9.jpg`, `hud_player_hp.png`,
  `bars.txt`, `match_take3_vs_earlier.txt`):

| take | time (s) | f60 | ticks | join | evidence | content |
|---|---|---|---|---|---|---|
| 1 | 0.000–1.617 | 0–97 | 0–32 | (start) | frames 0–8 identical (playback was paused; a grey YouTube ▶ resume icon sits mid-screen 0.30–1.15 s); player HP 21200/21200, boss bar 100 % (x 712–1207) | end of **3연속 포격**: the boss emerges from under the water and fires the **3rd shell** |
| 2 | 1.633–8.683 | 98–521 | 33–174 | **hard cut** at f98 (diff 41) | player HP jumps 21200 → **14419** across the cut (damage taken off-screen); boss bar 100 % → 99.3 % at 2.5 s → 98.4 % at 7.5 s | **꼬리 공격** (2 tail swings), then the boss stands upright |
| 3 | 8.700–14.53 | 522–872 | 174–291 | **jump cut** at f522 (diff 23) | same fight: boss bar stays 98.4 %; player HP 16945 → 19471 = exactly one more Barbara heal tick (+2526, the previous one was at 6.0–6.5 s) → ≈ 2–3 s removed | **가시 발사**, then the boss burrows (start of 이동 돌진) |
| 4 | 14.53–15.68 | 872–940 | 291–314 | **cross-dissolve** 14.53–14.62 + audio cut (BGM stops at 14.54, −20…−30 dB) | different party (케이아 active, 로자리아 / 디오나 / 바바라, HP 16685/16685), "모험 등급 59" badge top centre | **not the boss**: overworld run through a yellow giant-leaf forest; a white outlined box draws in 15.42–15.65 (x 465–1626, y 363–622) = the start of the next chapter's title card (`sheet_take4_titlebox_14.9-15.67.jpg`, `k_f0939_take4_new_scene.jpg`) |

  **No slow motion and no replays**: no alternating-duplicate (0.5×) runs anywhere; content matching of take 3 against takes 1–2 finds
  no repeated frames (errors ≈ 20 = different pictures). w1: one continuous take (spikes at f264 / f343 are the blast and dome-pop
  flashes). w2: shot cuts at f103 (4.12 s), f181 (7.24 s), f286 (11.44 s), f409 (16.36 s); f266 (10.64 s) and f440 (17.60 s) are
  in-scene flashes; fade to black 19.36–19.52 s.

### Editor captions in v6 (bottom-left: yellow slanted bar + bold white title + 1–2 white lines) — verbatim (`captions_v6_all.jpg`, `captions_metrics.txt`)

| # | on screen (s) | title | body (verbatim) | wiki name |
|---|---|---|---|---|
| 1 | already up at 0.00 (began in v5) → text slides out 0.25–0.88 → yellow block 0.67–1.37 → bar gone 1.58 | **3연속 포격** | 세 번의 포격을 날린다 / 첫 번째 포격 속도가 유난히 빠르다 | **증폭의 풀** ("fires several shells at the player in a row") |
| 2 | yellow line 2.05 → block 2.4–2.95 → text readable 3.43 → text out 7.35–7.75 → block 7.7–8.2 → gone 8.40 | **꼬리 공격** | 꼬리를 2회 후려친다 | **생명의 꼬리** (2 tail swings) |
| 3 | line 8.83 → block 9.47 → text readable 9.92 → text out 13.70–13.85 → block → gone with the dissolve at 14.5 | **가시 발사** | 가시를 여러 개 소환하고 한꺼번에 날린다 / 회피가 다소 난해한 편 | **생명의 나선** (mass spikes; the trails are literally spirals) |

Meanings: 1 = "fires three shells; the first shell is unusually fast"; 2 = "lashes the tail twice"; 3 = "summons many thorns and fires
them all at once; rather hard to dodge".

### In-game text

* v6 boss HUD: name **기원 오아시스의 파수꾼** (white, y ≈ 32), subtitle **「불씨」를 받아 소생한 생명** (light grey, y ≈ 62), "Lv.90",
  red bar **#FC5852** x 712–1207 at y 82–91 with dark-red track **#9C5131** and olive vine end caps (same frame as phase 1).
* Player bar bottom centre, green **#98CE37**: 21200/21200 → 14419 (take 2) → 16945 at 6.3 s (heal "+2526", green, beside the boss)
  → 19471 at 8.7 s (`hud_player_hp.png`). **The boss hits the player nowhere in v6**, so v6 gives no damage values.
* Party damage numbers: green "5432", "2526", "6418" on the boss (party hits; green tint = the arena's haze).
* **w1 banner** (dark translucent strip across the upper third, y ≈ 80–95 of 300 ≈ 290–340 at 1080p): **"소생의 찬가 보호막 안으로 들어가서
  종말의 여파를 막아내세요"** — "소생의 찬가 보호막" in red, the rest white (verbatim; confirmed against the sharp 1080p banner in the v5
  neighbour's `v5/banner_text.jpg`). White wipe line 0.84–0.96 s, flash 0.96–1.04 s, fully readable 1.24 s → fades 13.72–13.88 s
  (it stays up for the whole pattern, ≈ 12.6 s). = "Get inside the Hymn-of-Revival shield to block 종말의 여파".
* w1 green **"1048"** numbers next to the player at 6.60–7.52 s (≈ 8 numbers, one every 0.12–0.25 s; `sheet_w1_ticks_f158-f195_crop.jpg`).
  w1 has no player HP bar, so it is not provable whether these are Dendro field ticks taken or heal ticks; they start the moment
  the field ring passes the player and stop once she is inside the dome, so **treat them as the field's tick damage** (medium
  confidence).

## 1. Mapping to the wiki

| clip / time | what | wiki pattern |
|---|---|---|
| v6 0.00–1.62 | burrowed boss surfaces, charges, 3rd shell flies and lands left of the player | **증폭의 풀** (3연속 포격), shell 3 only (shells 1–2 are in v5) |
| v6 1.63–6.30 | crawl form, tail swing 1 (spin), coil upright, lunge + tail swing 2 | **생명의 꼬리** (꼬리 공격) |
| v6 6.30–8.68 | upright form, idle, facing the player at close range | (idle / punish window) |
| v6 8.70–9.90 | crawl form stands up and unfolds into the upright form (charge streaks) | wind-up of **생명의 나선** |
| v6 9.90–12.80 | ≈ 14 glowing seed-orbs appear around the boss, flare, then all fly at the player on double-helix trails; late leaf blades | **생명의 나선** (가시 발사) |
| v6 13.00–14.53 | hunch, sink into the water, leaf-pad trail travels across the lake (cut before it surfaces) | start of **이동 돌진** |
| w1 0–16.2 | banner → crouch/charge → rear-up loop → landing → light columns mark domes → field ring spreads → domes form → blast → domes pop | **종말의 여파** (field + dome shelter + near-lethal AoE) |
| w2 0–19.5 | golden egg (revived Heart) rises from its root nest; an ember; the egg is wrapped by vines and turns green; flash; arena; the Warden of Oasis Prime emerges | **phase 2→3 cut-scene** (소생 단계 → 기원 오아시스의 파수꾼) |

Not in these clips: all phase-1 patterns (잠복 돌진, 생명의 손, 발광하는 파수꾼, 초목이 시든 풍경, phase-1 생명의 꼬리, 근접 콤보,
소생 단계 진입), the whole phase-2 organism set and the Heart progress bar, the warning message, the surfacing hit of 이동 돌진,
shells 1–2 of 증폭의 풀, death.

**Phase 3 has two stances** (new in v6, important for the rig): a **crawl form** (armoured, quadruped/serpentine, dark green
hood-plates closed — looks like phase 1 but with lime-green crystals) used for moving, burrowing, shells and tail swings, and an
**upright form** (the plates open; a tall plant-woman with a glowing face, gold chest, six pale arms) used for 생명의 나선, idle and
종말의 여파. The change crawl → upright takes ≈ 0.7 s (v6 9.20–9.90).

## 2. Timelines (real time)

### 2.1 증폭의 풀 / 3연속 포격 — shell 3 (v6 take 1, 0.00–1.62 s), S0 = 0.75 s (t15)
Sheets: `sheet20fps_t1_shell3_0.00-1.62.jpg`, `sheet_perframe_shell3_launch_0.83-1.30.jpg` (60 fps), `sheet_perframe2_shell3_0.70-1.62.jpg`;
keys `k_v6_f0054…f0090`; zoom `zoom/zoom_f0060_shell3_flight.jpg`.

| event | s | f60 | tick | S+ t | notes |
|---|---|---|---|---|---|
| paused frame / resume (YouTube ▶) | 0.00–0.15 | 0–9 | 0–3 | — | the boss is under the water (it burrowed after shell 2 in v5); caption 1 still up |
| camera pans right toward a leaf splash on the water | 0.60–0.75 | 36–45 | 12–15 | | |
| **boss surfaces** in crawl form at the right, broadside, leaves and water splash around it (r ≈ 3 m) | 0.75 | 45 | 15 | 0 | `k_v6_f0054` |
| **charge**: body lights up pale yellow-green from inside, bright rim on the plates | 0.83–0.95 | 50–57 | 17–19 | +2…+4 | `k_v6_f0057` — the only tell, **≈ 4 t** |
| **launch**: flash on the body, a flat horizontal band of light (≈ 1.5–2 m tall, screen-wide) whips leftwards out of the body at body height | 0.95–1.10 | 57–66 | 19–22 | +4…+7 | `k_v6_f0060`; the shell is a fast flat streak, not a lob |
| **impact**: white light column at the far left edge (≈ 6–8 m to the player's left) | 1.10–1.15 | 66–69 | 22–23 | +7…+8 | `k_v6_f0066`; launch → impact **≈ 3 t** |
| burst: yellow-green leafy explosion + spray, r ≈ 2–3 m, fading | 1.15–1.33 | 69–80 | 23–27 | +8…+12 | `k_v6_f0078`; audio crack 1.46–1.55 s (high +7, air +9) |
| boss turns its head toward the camera (close side view of the hood) | 1.40–1.62 | 84–97 | 28–32 | | `k_v6_f0090`, `zoom/zoom_f0090_t1_body_side.jpg` |

The player (≈ 10 m from the camera, ≈ 8–10 m from the boss) was not hit (HP stays 21200). With the caption ("the **first** shell is
unusually fast") and v5 (shell 1 = a column falling on the player): shells are fired from the crawl form right after it surfaces;
each lands as a **light column + burst r ≈ 2–3 m**. Shell 3 here: tell 4 t, flight ≈ 3 t over ≈ 15–20 m (≥ 5 blocks/t).
Suggested MC: `burrow-move → surface → shell` ×3; telegraph each landing with a 4–6 t ground ring at the target (the original barely
telegraphs; ours must, because 3 t flight is undodgeable on reaction).

### 2.2 생명의 꼬리 / 꼬리 공격 (v6 take 2, 1.63–6.30 s), T0 = 3.10 s (t62)
Sheets: `sheet10fps_t2_1.63-4.50.jpg`, `sheet10fps_t2_4.50-8.68.jpg`, `sheet_perframe2_t2_1.63-2.80.jpg`,
`sheet_perframe2_tail1_3.10-4.30.jpg`, `sheet_perframe2_tail2_5.05-6.25.jpg`; zooms `zoom_f0099_t2_rear_close`,
`zoom_f0165_t2_crawl_tail_up`, `zoom_f0165_t2_crawl_side_scale`, `zoom_f0207_tail1_swing`, `zoom_f0330_tail2_swing`.

| event | s | f60 | tick | T+ t | notes |
|---|---|---|---|---|---|
| cut-in: boss very close, rear 3/4 view, half-reared, tail curled on the water at left | 1.63–2.00 | 98–120 | 33–40 | −29…−22 | `k_v6_f0099`; best close-up of tail + mantle plates |
| turns, crawls right broadside (≈ 3–4 m), tail raised over the back like a scorpion's | 2.00–3.10 | 120–186 | 40–62 | −22…0 | `k_v6_f0129`, `k_v6_f0165`; crawl ≈ 3 m/s |
| **tell 1**: body coils low, green glints run over the dark plates | 3.10–3.30 | 186–198 | 62–66 | 0…+4 | `k_v6_f0198` |
| body **spins in place** (≈ 180–270°, clockwise seen from the camera) | 3.30–3.47 | 198–208 | 66–69 | +4…+7 | `k_v6_f0204` |
| **SWING 1 active**: a broad yellow-green crescent of light sweeps right → left in front of the boss, ground level to ≈ 3 m high, leaving the frame on the left (radius ≥ 8–10 m) | 3.40–3.80 | 204–228 | 68–76 | +6…+14 | `k_v6_f0214`, `k_v6_f0222`; trail lingers to 4.0 s |
| leaf/glitter debris, body unwinds | 3.80–4.10 | 228–246 | 76–82 | +14…+20 | audio rustle/air bursts 3.9–4.7 s |
| **rears up into an S-curve**, tail lifted high (tell 2) | 4.10–5.05 | 246–303 | 82–101 | +20…+39 | `k_v6_f0282`, `k_v6_f0306` (≈ 0.95 s) |
| **lunges forward** (topples toward the player, ≈ 3–5 m) | 5.05–5.33 | 303–320 | 101–107 | +39…+45 | `k_v6_f0321` |
| tail-tip flash | 5.33–5.42 | 320–325 | 107–108 | +45…+46 | `k_v6_f0327` |
| **SWING 2 active**: crescent sweeps left → right low across the player's spot (the band passes over her at 5.45–5.55, no damage) | 5.42–5.65 | 325–339 | 108–113 | +46…+51 | `k_v6_f0333` |
| glitter shower (sparkles, leaf flakes) over ≈ 10 m | 5.65–6.00 | 339–360 | 113–120 | +51…+58 | `k_v6_f0345`; audio crackle 6.0–6.55 s |
| stands up into the upright form behind the player | 6.00–6.30 | 360–378 | 120–126 | +58…+64 | `k_v6_f0372` |
| upright idle, facing the player at ≈ 2–4 m (punish window) | 6.30–8.68 | 378–521 | 126–174 | | `k_v6_f0420`, `k_v6_f0480` |

Key numbers: tell 1 ≈ 4 t + spin 3 t → swing 1 at T+6…+14; swing 2 ≈ **40 t (2.0 s) after swing 1**, tell 2 = rear-up + lunge
(≈ 25 t); total ≈ 64 t; reach ≈ 9–11 m from the body axis, height 0–3 m, arc ≈ 180–270°. Hit body part = the tail (white segmented
underside; the light crescent is its trail). Safe zones: far (> 11 m), or jump/dash through the band; standing right at the body
during swing 2 is unsafe (the lunge covers 3–5 m).

### 2.3 생명의 나선 / 가시 발사 (v6 take 3, 8.70–12.80 s), N0 = launch 11.40 s (t228)
Sheets: `sheet10fps_t3_8.70-11.50.jpg`, `sheet_perframe2_t3_8.70-9.90.jpg`, `sheet20fps_t3_spikes_11.30-12.80.jpg`; keys
`k_v6_f0522…f0768`; zooms `zoom_f0528_t3_ghost_crouch` (crawl form, best plate/crystal view), `zoom_f0588_t3_rise_mantle`,
`zoom_f0672_t3_spikes_air` (orbs), `zoom_f0699_t3_spike_fire` (helix trails), `zoom_f0711_t3_spike_impacts`, `zoom_f0756_t3_leaf_blades`;
full `full/f0660.png`, `f0672`, `f0684`, `f0699`, `f0711`, `f0714`; grid `measure/grid_f0660_orbs.jpg`.

| event | s | f60 | tick | N+ t | notes |
|---|---|---|---|---|---|
| cut-in: crawl form, half-raised on its hind part, tail coiled on the water in front, ≈ 6–8 m from the player | 8.70–9.15 | 522–549 | 174–183 | −54…−45 | `k_v6_f0522`; audio thump 8.82–8.93 (low +10) |
| **charge**: yellow-green light streaks run along the body | 9.15–9.50 | 549–570 | 183–190 | −45…−38 | `k_v6_f0558` |
| **unfolds into the upright form**: plates open, six pale arms and yellow petal hands spread, mantle flares | 9.50–9.90 | 570–594 | 190–198 | −38…−30 | `k_v6_f0576`; dense crackle 9.2–10.3 s (high/air +7…+12) |
| **seed-orbs appear** around the boss (glowing yellow-green balls with a spiral glyph), ≈ 12–16, spread ±7 m sideways and 3–12 m up, slowly bobbing | 9.90–11.00 | 594–660 | 198–220 | −30…−8 | `k_v6_f0600`, `k_v6_f0672`, `k_f0660_spikes_summoned_full.jpg` |
| **tell**: 4-point star flares (lens glints) on the orbs | 11.00–11.35 | 660–681 | 220–227 | −8…−1 | `k_v6_f0660` |
| **launch**: orbs dart at the player one after another, each drawing a **double-helix ribbon trail** (DNA-like, two twisted strands) | 11.40–11.70 | 684–702 | 228–234 | 0…+6 | `k_v6_f0684`, `k_v6_f0690` |
| **impacts** around the player's position: yellow star bursts + upthrust crystal/leaf spikes, 8–14 of them | 11.55–12.25 | 693–735 | 231–245 | +3…+17 | `k_v6_f0699`, `k_v6_f0711`; audio thumps 11.9–12.6 (low +10…+11) |
| dark leaf debris splashes, settling | 12.25–12.50 | 735–750 | 245–250 | +17…+22 | `k_v6_f0726` |
| 2–3 **leaf blades** (big pale-yellow translucent leaves, ≈ 2–2.5 m long) skim low across the area, left → right | 12.50–12.80 | 750–768 | 250–256 | +22…+28 | `k_v6_f0768`, `zoom_f0756_t3_leaf_blades` |

Key numbers: unfold 8 t; orbs float ≈ 1.5 s (30 t) before launch; flare tell 7 t; launch window ≈ 6 t; projectile flight ≈ 3–6 t
(15–20 m → ≈ 3–5 blocks/t); impacts over ≈ 14 t; total from charge to the last blade ≈ 3.6 s (73 t). Homing: every trail converges
on the player's position at launch; the running player was trailed by ≈ 1–3 m (no mid-flight steering visible). Impact area per
spike ≈ r 1.5–2 m; the cluster covers r ≈ 4–5 m around the target. The player was not hit (HP stays 19471). Safe: keep running
sideways during the 6-t launch window.

### 2.4 이동 돌진 — start only (v6 take 3, 13.00–14.53 s)
Sheets: `sheet10fps_t3_12.80-14.65.jpg`, `sheet20fps_t3_burrow_12.80-14.60.jpg`; zooms `zoom_f0780_t3_hunch_burrow_start`,
`zoom_f0804_t3_burrow`; grid `measure/grid_f0780.jpg`, `measure/grid_f0804.jpg`.

| event | s | f60 | tick | notes |
|---|---|---|---|---|
| upright idle, dark ring of leaves on the water around the stem (⌀ ≈ 6.5–7.5 m) | 12.60–13.00 | 756–780 | 252–260 | `k_v6_f0756` |
| hunches down (arms forward, hood lowered) | 13.00–13.35 | 780–801 | 260–267 | `zoom_f0780` |
| **sinks into the water** in a burst of green light + leaf splash (⌀ ≈ 6.5–9 m) | 13.35–13.60 | 801–816 | 267–272 | `k_v6_f0792`; audio low +7…+11 13.4–14.05 |
| gone; green mist column fades | 13.60–13.90 | 816–834 | 272–278 | `k_v6_f0816` |
| **underground travel**: a trail of yellow lily-pad leaves surfaces along its path across the lake, ≈ 8–15 m/s | 13.90–14.53 | 834–872 | 278–291 | `k_v6_f0852`; cut before it surfaces |

The surfacing attack is not shown (the wiki: it bursts out at the player's position; v6 take 1 shows a surfacing with a splash r ≈ 3 m
right before shell 3). Total sink ≈ 12 t, underground ≥ 0.6 s.

### 2.5 종말의 여파 (w1, 25 fps, one take), banner B0 = 0.84 s (t17)
Sheets: `sheet4fps_w1.jpg`, `sheet8fps_w1_f0-f100.jpg` … `f300-f405`, `sheet_w1_every2_f80-f130.jpg`, `sheet_w1_every2_f130-f192.jpg`,
`sheet_w1_every2_f195-f255.jpg`, `sheet_w1_every2_f310-f335_f365-f405.jpg`, `sheet_w1_perframe_f335-f365.jpg`,
`sheet_w1_ticks_f158-f195_crop.jpg`; keys `keys/k_w1_*`; zooms `zoom_f0127_w1_core_glow_orange`, `zoom_f0152_w1_field_ring`,
`zoom_f0166_w1_tick_dome_left`, `zoom_f0184_w1_dome_formed`, `zoom_f0270_w1_blast`, `zoom_f0330_w1_three_domes`,
`zoom_f0375_w1_upright_scale_nahida`.

| event | s | f25 | tick | B+ t | notes |
|---|---|---|---|---|---|
| upright idle, player (나히다) ≈ 8–10 m in front | 0.00–0.84 | 0–21 | 0–17 | | `k_w1_f0000` |
| **banner** wipes in (white line → flash → text readable at 1.24) | 0.84–1.24 | 21–31 | 17–25 | 0…+8 | `k_w1_f0024`, `k_w1_f0030` |
| sinks into a low crouch, water splashes at the base | 1.10–1.90 | 27–48 | 22–38 | +5…+21 | `k_w1_f0045` |
| low crouch, leaves fanned out flat on the water around it (r ≈ 3–4 m), faint green light column above it | 1.90–3.00 | 48–75 | 38–60 | +21…+43 | `k_w1_f0066` |
| rises, arms up | 3.00–3.60 | 75–90 | 60–72 | +43…+55 | `k_w1_f0087` |
| **rears into a loop**: the body arches over into a full ring, mantle leaves whirl | 3.60–4.50 | 90–113 | 72–90 | +55…+73 | `k_w1_f0096` |
| lands crouched, a ring of leaves forms on the water | 4.50–5.00 | 113–125 | 90–100 | +73…+83 | `k_w1_f0110`, `k_w1_f0118` |
| **core/face glows orange-gold** | 5.00–5.30 | 125–133 | 100–106 | +83…+89 | `k_w1_f0127` |
| stands, spreads the mantle | 5.30–5.60 | 133–140 | 106–112 | +89…+95 | |
| **white light column** on the water at the left (= a dome spot) + splash | 5.68–5.90 | 142–148 | 114–118 | +97…+101 | `k_w1_f0142` |
| **field ring released**: a flat translucent yellow-green wave races outward over the water from the boss; reaches the player (≈ 9 m) at ≈ 6.1 s (≈ 25 m/s) and the ground stays tinted | 5.90–6.20 | 148–155 | 118–124 | +101…+107 | `k_w1_f0150`, `k_w1_f0156` |
| first dome visible at the left, a second further left | 6.40–6.60 | 160–165 | 128–132 | +111…+115 | `k_w1_f0160` |
| "1048" ticks at the player (≈ every 0.12–0.25 s) | 6.60–7.52 | 165–188 | 132–150 | +115…+133 | `k_w1_f0166` |
| big white-yellow burst right at the player + light column (the dome spot she ran to) | 6.68–6.85 | 167–171 | 134–137 | +117…+120 | `k_w1_f0168` |
| **dome forms around the player**: vertical light lines rise, a hemisphere grows from the ground up | 7.28–7.60 | 182–190 | 146–152 | +129…+135 | `k_w1_f0178`, `k_w1_f0182`, `k_w1_f0184`; dome r ≈ 3 m |
| inside the dome; boss stalks around it, its tail sweeps over the dome (no effect) | 7.60–10.50 | 190–262 | 152–210 | +135…+193 | `k_w1_f0205`, `k_w1_f0230` |
| **BLAST**: white flash, white rays | 10.56–10.84 | 264–271 | 211–217 | +194…+200 | `k_w1_f0264`, `k_w1_f0270` |
| yellow flood over the whole field outside the domes; light pillars shoot up | 10.88–12.00 | 272–300 | 218–240 | +201…+223 | `k_w1_f0280`, `k_w1_f0290` |
| aftermath: **three domes** standing on the lake, field fading | 12.00–13.68 | 300–342 | 240–274 | +223…+257 | `k_w1_f0330` |
| **domes pop** (white flash, shards), banner fades | 13.72–14.10 | 343–352 | 274–282 | +257…+265 | `k_w1_f0343`, `k_w1_f0348` |
| boss upright idle in front of the player | 14.10–16.24 | 352–406 | 282–325 | | `k_w1_f0375` |

Key numbers (for MC): banner → field release **≈ 5.0 s (101 t)** of wind-up (crouch, loop, landing, orange core = the readable tells);
field release → blast **≈ 4.6 s (93 t)**; dome lifetime ≈ 7.3 s (first dome 6.4 s → pop 13.72 s); the dome stays **≈ 3.2 s (63 t) after
the blast**; whole pattern ≈ 13.3 s (≈ 265 t). Domes: ≥ 3 at fixed spots on the lake (left, centre, right of the player), r ≈ 3 m
(2.5–4), each marked first by a white light column; standing inside = immune to the blast. Field: covers the whole lake; small
ticks while outside a dome. Blast: whole arena outside domes, near-lethal.

### 2.6 Phase 2→3 cut-scene (w2, 25 fps)
Sheets: `sheet4fps_w2.jpg`, `sheet8fps_w2_f0-f105.jpg` … `f400-f487.jpg`; keys `keys/k_w2_*`; zooms `zoom_f0030_w2_egg_nest`,
`zoom_f0075_w2_egg_rising`, `zoom_f0140_w2_twig_spark`, `zoom_f0195_w2_egg_canopy`, `zoom_f0240_w2_egg_tendrils`,
`zoom_f0350_w2_arena_wide`, `zoom_f0415_w2_p3_hood_side`, `zoom_f0430_w2_p3_chest_crown`, `zoom_f0475_w2_p3_reveal`.

| shot | s | f25 | tick | content |
|---|---|---|---|---|
| S1 | 0.00–4.08 | 0–102 | 0–82 | dark gold cave: the **golden egg** lies tilted in a nest of dark twisted roots (6–8 root "fingers" with glowing teardrop buds) on cracked earth, faint gold ring glyph around; gold motes. 1.6–2.5 s it lifts and turns upright, gold ripples on the floor; 2.5–4.1 s rises out of frame, dripping gold strands and droplets |
| S2 | 4.12–7.20 | 103–180 | 82–144 | darkness: a pale dead twig with an **ember** (gold spark) at its tip, orange shelf mushroom below; the ember crawls along the twig, sparks rising (= the 「불씨」 of the subtitle) |
| S3 | 7.24–11.40 | 181–285 | 145–228 | the egg, upright, seen inside a cup of huge yellow translucent leaves; 8.4–9.5 s green vines grow over its top like a grasping hand/crown; 9.5–10.6 s the light turns from gold to green with cyan streaks; **10.68 s flash**; 10.8–11.4 s green lightning ribbons around the vine-wrapped egg |
| S4 | 11.44–16.32 | 286–408 | 229–326 | **wide arena shot**: round lake ringed by giant trees with buttress roots, a dome of huge veined leaves overhead; a green lightning "flower" bursts in the air over the lake centre (11.4–12.6 s) and leaves a glowing orb hanging there; yellow bulb-flowers light up on the bank (14.3 s →) |
| S5 | 16.36–19.36 | 409–484 | 327–387 | **emergence**: burst of yellow-green leaves, the dark hood rises (16.4–16.7), hood side close-up (16.7–17.0), pan up the mantle to the **gold leaf crown around a glowing pale-yellow face** (17.2–17.6), **green lightning flash 17.68 s**, reveal 17.8–19.3 s: the upright Warden towers over the Traveler and 나히다 (bottom left); fade to black 19.36–19.52 |

For MC: egg-rise 4 s, ember 3 s, greening 4.2 s, arena 4.9 s, emergence 3 s ≈ 19.5 s total — a short version (≈ 8–10 s: egg lifts →
vines + flash → leaf burst → reveal) keeps the beats.

## 3. Size (player = 1.7 m ruler; "PH" = player heights)

Method: `measure/grid_*.jpg` give pixel rows/columns; `v6w_tools/sizefit.py` fits a pinhole camera (vertical FOV 45°, f ≈ 1304 px) to
the player (1.7 m, foot and head rows) for several camera heights h and returns the boss part sizes from its ground-contact row.
The camera height is not observable directly, so h is bracketed by requiring the far lake shore to come out at ≈ 15–25 m (it is the
same lake in every frame). Barbara's real model is ≈ 1.5 m: with her true height every number shrinks by ≈ 12 %.

| item | frames | estimate | range | PH | notes |
|---|---|---|---|---|---|
| **upright form, crown/hood top** | f0480 (`sizefit_f0480.txt`), f0756, f0420 | **≈ 8 m** | 7–9 | 4.7 | base hidden behind the player at row ≈ 820; same-depth lower bound 5.6 m |
| upright, raised petal-hand tips | f0480 | **≈ 8.8 m** | 7.6–9.4 | 5.2 | upper arm pair raised |
| upright, arm span (outer petal tip to tip) | f0480, f0756, w1 f375 | **≈ 10 m** | 9–11.5 | 6 | w1 with 나히다 (1.25 m) as ruler: 10.8–13 m |
| head (hood incl. hanging leaf-hair), width | f0480 | ≈ 3 m | 2.5–3.5 | 1.8 | |
| glowing face mask, height | f0480 | ≈ 1.8 m | 1.4–2.2 | 1.1 | |
| gold chest/sternum plate, length × width | f0480 | ≈ 2.3 × 0.8 m | ±30 % | | segmented, 6–8 chevron ribs |
| yellow petal hand (broad leaf "hand") | f0480, f0672 | ≈ 2–2.5 m long | ±30 % | 1.3 | |
| leaf ring on the water around the stem, ⌀ | f0756 | ≈ 6.5–7.5 m | | | |
| **crawl form, hood top** | f0165 (`grid_f0165.jpg`) | **≈ 5–6 m** | 4.5–6.8 | 3.2 | camera h 3.5–4 m bracket |
| crawl form, body length (rear petals → head) | f0165 | **≈ 12–14 m** | 11–15 | 7.6 | = 1 BL below |
| crawl form, length incl. tail | f0165, f0099 | ≈ 13.5–16 m | | 8.8 | tail ≥ 5 m, segmented, ⌀ ≈ 0.6–0.8 m |
| hunched (pre-burrow), hood top / burst ⌀ | f0780 | 5.4–6 m / 6.4–7 m | | 3.4 | |
| tail-swing reach (from body axis) | take 2 | ≈ 9–11 m | | ≈ 0.75 BL | crescent leaves the frame |
| seed-orb (생명의 나선) diameter | f0672 | ≈ 0.6–0.8 m | | 0.4 | 12–16 orbs |
| leaf blade (late spike) | f0756 | ≈ 2–2.5 m long, 0.8 m wide | | 1.3 | |
| shell burst radius | f0078 | ≈ 2–3 m | | | |
| w1 dome (보호막) radius | w1 f184 (`grid_w1_f0184.jpg`, 나히다 inside) | **≈ 3 m** | 2.5–4 | | hemisphere, ⌀ ≈ 6 m |
| w1 field ring | w1 f150–156 | whole lake | | | ≥ 20 m radius |
| golden egg (w2) | — | no ruler in w2; use the neighbours' Heart size (v2/v4: ≈ 2 m tall bulb) | | | aspect ≈ 1.25 : 1, lemon-shaped |

**Best estimate**: phase 3 upright ≈ **8 m tall (± 1), 10 m arm span**; phase 3 crawl ≈ **5–6 m tall, 12–14 m long (+ tail)** —
the crawl form is the same size class as phase 1 (neighbours: 4.3–4.7 m crouch, 13–16 m with tail), the upright form is ≈ 1.7×
taller. Caveat: the ellipse-aspect method on the leaf ring in f0756 hints at an even larger boss (12–17 m) but is biased by the
ring's thickness and shape; the shore-consistent camera fit is preferred. MC: 1 m = 1 block gives an 8-block upright boss in an
r ≈ 20–24 arena; a 0.8–0.85 build scale (upright ≈ 6.5–7 blocks) keeps the proportions (design choice).

## 4. Model notes

Colours are sampled from v6 full frames (`pts_*.txt`, `pal_*.txt`). **The whole phase-3 arena is under a strong green haze**: every
sample is pushed toward green; desaturate/neutralise by ≈ 15–25 % for textures. w1/w2 colours (`pal_w1w2.txt`) are low-res and only
approximate.

Best frames for modelling:

| file | shows |
|---|---|
| `zoom/zoom_f0480_t2_stand_front.jpg`, `keys/k_v6_f0480_t2_upright_front_best.jpg`, `full/f0480.png` | **upright form, front, closest — the reference** (face, crown, chest plate, six arms, skirt, player for scale) |
| `zoom/zoom_f0672_t3_spikes_air.jpg`, `full/f0672.png` | upright front with all arms spread + the seed-orbs |
| `zoom/zoom_f0420_t2_upright_side.jpg`, `full/f0420.png` | upright, 3/4 side, S-curve of the body, arm layering |
| `zoom/zoom_f0588_t3_rise_mantle.jpg`, `full/f0588.png` | crawl → upright unfolding (plates opening) |
| `zoom/zoom_f0528_t3_ghost_crouch.jpg` | **crawl form, 3/4 front: dark plates with lime crystals, curled yellow limbs, white banded tail** |
| `zoom/zoom_f0099_t2_rear_close.jpg`, `full/f0099.png` | crawl form from behind, very close: plate layering, tail root |
| `zoom/zoom_f0165_t2_crawl_side_scale.jpg`, `zoom_f0165_t2_crawl_tail_up.jpg`, `full/f0165.png` | crawl form broadside, tail raised, player for scale |
| `zoom/zoom_f0090_t1_body_side.jpg`, `full/f0090.png` | crawl form head/hood close-up, crystals |
| `zoom/zoom_f0780_t3_hunch_burrow_start.jpg`, `full/f0780.png` | hunched upright before burrowing |
| `zoom/zoom_f0756_t3_leaf_blades.jpg`, `full/f0756.png` | upright from further back + leaf ring + leaf blade |
| `zoom/zoom_f0475_w2_p3_reveal.jpg`, `keys/k_w2_f0475_reveal_full_body.jpg` | cinematic full body (gold crown, chest) |
| `zoom/zoom_f0430_w2_p3_chest_crown.jpg`, `keys/k_w2_f0436_crown_gold_flower.jpg` | **gold leaf crown around the glowing face (back/side)** |
| `zoom/zoom_f0415_w2_p3_hood_side.jpg`, `keys/k_w2_f0418_hood_side_closeup.jpg` | hood side with crystals at emergence |
| `zoom/zoom_f0030_w2_egg_nest.jpg`, `zoom_f0075_w2_egg_rising.jpg`, `zoom_f0195_w2_egg_canopy.jpg`, `zoom_f0240_w2_egg_tendrils.jpg` | **golden egg**: in the root nest, rising, in the leaf cup, wrapped by vines |
| `zoom/zoom_f0350_w2_arena_wide.jpg`, `keys/k_w2_f0300_energy_flower_sky.jpg` | arena layout (lake, giant trees, leaf dome) |
| `zoom/zoom_f0184_w1_dome_formed.jpg`, `zoom_f0330_w1_three_domes.jpg` | dome look and count |

### 4.1 Phase 3, upright form (기원 오아시스의 파수꾼) — parts top → bottom (sizes from §3)
1. **Gold leaf crown** (w2 f430/f436, w1 f375): a ring of 8–10 bronze-gold leaf petals standing up around the back/top of the head
   like a laurel/flower crown (≈ 2.5–3 m across), glowing tips. Gold ≈ **#D3BD49 / #F4DB60** (w2), shade #8C7533.
2. **Hood / hair**: a tall dome of hanging dark-olive leaf strands draping down both sides to the chest like long hair
   (#516718 / #4E691F / #316340, lit #8CA462), a small lime crystal spike on the upper right (#83D430).
3. **Glowing face mask** (≈ 1.8 m tall oval): pale yellow-green with an embossed leaf/flower emblem, emissive
   **#CCE384 / #B0C36D / #AECD6A**; turns **orange-gold** when charging 종말의 여파 (w1 f127: mean **#CB9151**, hot spots #F4DC1C; low-res, `measure/w1_f0127.png`).
4. **Neck & chest**: a vertical **gold segmented sternum/spine plate** with 6–8 chevron ribs (≈ 2.3 × 0.8 m), gold
   **#DBDE80 / #A4A64B / #939947**, framed by dark green bands and white bead-strings.
5. **Six arms in three pairs**, all pale grey-white limbs with dark vein lines (#B6C1B1 / #CAD5C2 / #B2D39B, vein dark #4C6E45):
   * upper pair raised up/out, gold cone spikes at the elbows and tips (#D1D143 / #D3E466 / #DFEE50);
   * middle pair spread wide, ending in **huge yellow leaf-petal hands** (≈ 2–2.5 m) — yellow **#C7D687 / #B0C273 / #99A553**, glowing
     edges #D6E490, white under-layer;
   * lower pair sweep down and out to the water like legs, also ending in yellow petal hands (they rest on the water).
   * strings of small white leaflets ("beads") hang along the arms (#E5F3EB).
6. **Skirt / stem**: a dark teal-black robe-stem (**#3D5447 / #2B4237 / #314645**, lit #466758) with an ornate front panel with gold
   curl inlays, standing in a ring of yellow leaves on the water (⌀ ≈ 7 m).
7. No visible legs or tail in this stance (the tail is folded into the stem).

### 4.2 Phase 3, crawl form — and the differences to phase 1
* Same body plan as phase 1 (neighbours v1/v2: hooded quadruped with petal hands, tail, mantle of leaf panels), but:
  * **crystals are lime-green** (#4DAF26 / #6DC928 / #62C52C, glow #B0D38C) instead of phase-1 gold-yellow (#FEF560);
  * plates are darker, greener **#294D27 / #396638 / #426A39 / #578757** with near-black rims (#255723) — phase 1 was grey-green
    #343A2F / #504F39;
  * limb petals are **yellow-tipped** (#A0B04A / #A8C469) and curl like fiddleheads; phase 1 petals were pale cream #B3AF9B;
  * **tail**: long, pale grey-white, segmented/banded like a centipede (**#ADB7AF / #A9B3A5 / #939E91**, dark band lines), ending in
    a thin whip; it lies coiled on the water or arches over the back like a scorpion's;
  * the head plate at the front is a dark grey "mantis" hood (#445440).
* Stance switches: crawl → upright by opening the plates (they fold back into the hair/mantle) and unrolling the arms (≈ 0.7 s);
  upright → crawl by hunching and closing them (≈ 0.35 s, v6 13.0–13.35).

### 4.3 The Heart / golden egg (w2)
* Lemon-shaped, smooth, translucent **golden egg** (aspect ≈ 1.25 : 1), soft inner highlights; **#F4DB60 / #F5E05E / #D3BD49 /
  #CFBC4A** (low-res). Lies tilted in a **nest of 6–8 dark twisted root fingers** (#31290C / #614B20) whose tips carry glowing gold
  teardrop buds; cracked dark-gold earth (#665223 / #927834, cracks #392D0D) with a faint gold ring glyph.
* States: idle glow → lifts upright, drips gold strands → wrapped by green vines (a "hand" crown) → turns green with cyan streaks →
  flash → (becomes the energy orb over the lake). For MC: egg = 1 item_display (custom model, emissive) + root-nest props + vine
  overlay card + colour swap gold → green.

### 4.4 FX colours (glow pixels, `pal_fx.txt`)
* Shell charge / band: **#E7F99F / #D2F18B / #ECFAB7**; landing column **#FDFBBD / #FBFBB7**; burst #D1E98D.
* Tail crescents: swing 1 **#A4D6AC / #BFE682 / #E5F5EA**; swing 2 **#EBF898 / #D7ED7A / #D6ECE2**; glitter #EBF898.
* Unfold streaks: #A9D57C / #CDE78A / #D1EAC2.
* Seed-orbs: body **#ABDE85 / #9CD68B**, flares **#E6F8A5 / #F6FBDE / #D9F096**; helix trails **#ECF9C9 / #C3DFA1 / #8BCAAA**;
  impacts **#D9E674 / #EDF597 / #C4D353 / #F6FBC2**.
* 종말의 여파 (w1, approximate): field ring #9BBE61 / #ACD075 / #C5E892; dome body #88BB5F / #B5DA72, rim #E4F69D; blast flash
  #F2FABA / #FBFCEB; yellow flood **#FBFAA4 / #DFEA59 / #E8E63E / #F5F573**.
* MC particle mapping: `dust{color:[0.85,0.95,0.55],scale:2}` + `end_rod` + `glow` for orbs and the face; `dust_color_transition`
  #E7F99F → #8BCAAA along helix paths (two sine-offset strands); `composter` + `falling_spore_blossom`/`cherry_leaves` for leaf
  debris; `flash` for impact columns and the blast; `happy_villager` / `wax_on` for glitter; a big `block_display` hemisphere of
  lime stained glass (or a textured item_display shell) for the dome; `spore_blossom_air` for the field.

### 4.5 Arena
* Round **forest lake**: shallow teal water as the floor (**#94CB80** near, **#75BDB6 / #5F9B72** mid; w2 #8FCEB2), dark root/crack lines
  on the lakebed, ringed by **giant trees** with buttress roots (#70A149 in the haze) and a **dome of huge veined translucent leaves**
  overhead (#97C574, dark veins), grassy banks with glowing yellow bulb-flowers and orange shelf mushrooms.
* Radius: far shore ≈ 15–25 m from the camera in v6 (fits) and the w2 wide shot shows a lake ≈ 2× the boss's arm span across at
  least → usable radius **≥ 20 m** (neighbours: ≥ 25–35 m). MC: r ≈ 20–24 water-floor disc (light-blue/cyan concrete powder? —
  better: prismarine/warped-wart-free mix under 1 layer of water, or waterlogged slabs), mangrove/jungle giant trunks at the rim,
  lime/green stained-glass leaf panels overhead, froglights/shroomlights as bulb-flowers, green fog.

### 4.6 HUD
* Boss bar (phase 3): unchanged layout, name **기원 오아시스의 파수꾼**, subtitle **「불씨」를 받아 소생한 생명**, red #FC5852.
* 종말의 여파 banner: dark translucent band across the upper third; red "소생의 찬가 보호막" + white "안으로 들어가서 종말의 여파를
  막아내세요"; shown from the start of the wind-up until the domes pop.
* No revival progress bar in these clips (phase 2 is covered by v4/v5).

### 4.7 Rig / display-entity hints (phase 3)
Two-stance rig: root (yaw) → stem (bend 2–3 segments) → chest (gold plate) → head (face emissive card + hair cards + crown ring of
8–10 petal cards) → arm_U/M/L × L/R (shoulder, elbow, petal hand of 3–5 leaf cards, bead strings) → skirt (4–6 hanging cards) →
water leaf-ring decal. Crawl stance reuses the phase-1 quadruped bones (hood, mantle plates ×6, forelimbs, rear limbs, tail ×6–8
segments) with the lime-crystal material set; plate cards that close over the upright parts make the stance swap a scale/rotation
animation rather than a model swap. Emissive parts (brightness 15): face, crown tips, crystals, petal edges, orbs.

## 5. Audio (v6 only; w1/w2 are silent)

Background: the uploader's BGM (steady tonal lines 200–1500 Hz in `speech_0-8.png`, `speech_8-15.6.png`) under everything; no voice
lines (no curved formants), no narration. SFX are broadband washes on top; onsets (`events.txt`, `bands_onsets.txt`, `onsets.txt`,
`spec_0-4.png` … `spec_12-15.6.png`). Audio lags the picture by ≈ 0.25–0.35 s.

| event (picture time) | audio | character | vanilla layers (Java 26.x names) |
|---|---|---|---|
| boss surfaces (0.75) | wash ≈ 0.9–1.2 | water slosh + rustle | `block.mud.break` + `entity.player.splash` (p 0.6) + `block.azalea_leaves.break` |
| shell charge (0.83–0.95) | — (in the wash) | rising shimmer | `block.respawn_anchor.charge` (p 1.5, v 0.6) + `block.amethyst_block.resonate` (p 1.6) |
| shell launch + streak (0.95–1.10) | | whoosh | `entity.breeze.shoot` (p 0.8) + `item.trident.riptide_1` (p 1.4, v 0.5) |
| shell impact (1.10–1.33) | 1.46–1.55 (high +7, air +9) | bright crack + leaf burst | `entity.generic.explode` (p 1.3, v 0.5) + `block.beacon.activate` (p 1.8) + `block.cherry_leaves.break` |
| tail swing 1 (3.40–3.80) | 3.9–4.7 (low +7…+9, air +7…+11) | heavy whoosh, rustling trail | `entity.player.attack.sweep` (p 0.5) + `entity.breeze.wind_burst` (p 0.7) + `block.azalea_leaves.fall` ×3 |
| rear-up / lunge (4.1–5.33) | 5.9–6.0 low | creak + thud | `entity.creaking.activate` (p 0.6) + `entity.ravager.step` (p 0.6) |
| tail swing 2 + glitter (5.42–6.0) | 6.0–6.55 (air +7…+10) | whoosh + sparkle crackle | as swing 1 + `block.amethyst_cluster.step` ×4 + `item.bone_meal.use` |
| emerge / cut-in (8.70–9.15) | 8.82–8.93 (low +10) | thump | `entity.warden.emerge` (p 1.3, v 0.5) + `block.rooted_dirt.break` |
| unfold + streaks (9.15–9.90) | 9.2–10.3 dense high/air (+7…+12) | crackle, rising | `entity.breeze.charge` (p 1.2) + `block.big_dripleaf.tilt_up` (p 0.6) + `block.amethyst_block.chime` ×3 |
| seed-orbs appear / hover (9.9–11.0) | 10.95, 11.33–11.43 low | soft pulses | `block.amethyst_cluster.place` per orb + `block.beacon.ambient` (p 1.8, v 0.3) loop |
| orb flares (11.0–11.35) | — | glints | `block.beacon.power_select` (p 1.8, v 0.5) |
| launch + helix flight (11.40–11.70) | — | whips | `entity.arrow.shoot` (p 0.6) per orb + `item.trident.throw` (p 1.4, v 0.4) |
| impacts (11.55–12.25) | 11.9–12.6 (low +10…+11, ≈ every 0.03–0.06 s) | thump chain | `entity.generic.explode` (p 1.6, v 0.3) + `block.amethyst_cluster.break` (p 0.8) + `block.pointed_dripstone.land` |
| leaf blades (12.5–12.8) | 12.8–13.1 (low +11…+13) | swoosh + rumble | `entity.breeze.wind_burst` (p 1.2) + `block.cherry_leaves.fall` |
| sink / burrow (13.35–13.9) | 13.4–14.05 (low +7…+11) | rumble, splash | `entity.warden.dig` (p 1.2) + `block.mud.place` + `entity.player.splash.high_speed` (p 0.6) |
| underground travel (13.9–14.5) | 14.0–14.4 low | rustle | `block.lily_pad.place` ×N along the trail + `block.big_dripleaf.tilt_down` |
| (w1) banner | — | — | `block.respawn_anchor.set_spawn` (p 0.7) + `entity.elder_guardian.curse` (p 1.4, v 0.4) |
| (w1) orange core / field release | — | — | `block.conduit.activate` + `entity.warden.sonic_charge` (p 1.4); ring: `entity.breeze.wind_burst` (p 0.6) + `block.grass.break` |
| (w1) dome spot column / dome forms | — | — | `block.beacon.activate` (p 1.8) + `block.amethyst_block.chime` ×3 + `block.respawn_anchor.charge` (p 1.6) |
| (w1) blast | — | — | `entity.warden.sonic_boom` (p 0.7) + `entity.generic.explode` (p 0.5) + `entity.lightning_bolt.thunder` (p 1.5, v 0.4) |
| (w1) dome pop | — | — | `block.glass.break` (p 1.3) + `block.amethyst_block.break` |
| (w2) egg / ember / flash / emergence | — | — | `block.beacon.ambient` (p 0.7) loop; ember `block.fire.ambient` (p 1.6, v 0.3); flash `block.beacon.activate` + thunder (p 2.0, v 0.3); emergence `entity.warden.emerge` (p 0.8) + `block.azalea_leaves.break` burst |

## 6. Implementation-oriented summary (20 tps; 1 m = 1 block before any build scale)

* **Stances**: crawl (move/burrow/shells/tail) and upright (spikes/idle/종말의 여파); swap crawl → upright 14 t, upright → crawl 7 t.
* **증폭의 풀 (3연속 포격)**: ×3 [burrow-move → surface (splash r 3) → charge 4 t → shell flies ≈ 3 t (fast, flat) → landing column +
  burst r 2–3 at the target]; give our version a 4–6 t ground marker before each landing; the first shell is the fastest (caption).
* **생명의 꼬리**: tell 4 t + spin 3 t → crescent sweep 8 t (r ≈ 10, h 0–3, 180–270°) → recover 6 t → rear-up S-coil 19 t → lunge
  3–5 m in 6 t → tail-tip flash 2 t → second sweep 5 t (opposite direction) → glitter 7 t → stand up 6 t (≈ 64 t total).
* **생명의 나선**: unfold 8 t (with charge streaks 7 t before) → spawn 12–16 orbs around the boss (±7 m, 3–12 m up) and hover 30 t →
  flare 7 t → launch all within 6 t at the player's current position, helix trail, flight 3–6 t → impacts r 1.5–2 each, cluster r 4–5
  over 14 t → 2–3 leaf blades skim low 6 t later. Total ≈ 73 t.
* **이동 돌진**: hunch 7 t → sink 5 t (burst ⌀ 7) → underground ≥ 12 t, leaf-pad trail at ≈ 0.4–0.75 b/t toward the player →
  surface at the player's position (not shown in v6; take-1 surfacing splash r ≈ 3).
* **종말의 여파**: banner on → wind-up 101 t (crouch 20 t, low crouch 22 t, rise 12 t, loop 18 t, land 10 t, orange core 6 t, stand 6 t)
  → mark ≥ 3 dome spots with light columns (r 3) → field ring sweeps the arena (≈ 1.25 b/t) and ticks small damage outside domes
  every ≈ 4 t → domes rise when the player enters (8 t to full) → blast at field + 93 t: near-lethal to everything outside the
  domes → domes persist 63 t → pop. Repeat later in the fight.
* **Cut-scene 2→3**: egg lift + rise → vines + gold-to-green → flash → leaf burst → reveal (8–10 s short version of w2's 19.5 s).
