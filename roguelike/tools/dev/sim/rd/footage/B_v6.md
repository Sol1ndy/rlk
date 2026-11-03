# B_v6 - footage log (v6.mp4, 40.1 s, 1080p60)

Analyst B. Ticks: `t = round(seconds x 20)` relative to the start of v6.
Source type: a Korean guide compilation. Each segment carries a burned-in caption
(pattern name + tip). v6 -> v7 -> v8 -> v9 look like one continuous recording split
into chunks (v6 ends on the "3단 콤보" caption and v7 opens mid-combo; v7 ends with
the sword waves in flight and v8 opens with them reaching the player; v8 ends inside
the instant-death dome and v9 opens there). Approx. global offsets: v7 = v6+40.1 s,
v8 = v6+80.5 s, v9 = v6+120.9 s (not frame-verified).

Scale: player character ~1.8 b tall (1 b = 1 m). Arena: flat, featureless floor
(teal shallow-water/sand texture in the Shogun phase; turns dark blue/violet after the
transformation); arena edge is never in shot in v6.
Audio: BGM has a steady beat of 0.455 s (~132 BPM); onsets on that grid are music and
were ignored. Attack SFX are the 4-10 kHz "crackle" peaks listed below (HF).
Contact sheets: `work/B/sheets/v6_2fps_0[1-4].jpg`, `v6_caps.jpg` (captions 1 fps),
dense strips `work/B/dense/v6_[a-h].jpg`, hi-res grids `work/B/hi/v6_*.jpg`.

## Segments (caption -> span)

| span (s) | ticks | caption | form |
|---|---|---|---|
| 0.0-1.0 | 0-20 | 마가츠의 뇌안 - "그냥 공격하여 부수면 스턴됩니다" | Shogun (sword) |
| 1.05-8.9 | 21-178 | 마가츠의 뇌안 2 - "하나를 골라 부수고 범위 밖에서 공격을 피합니다" | Shogun |
| 8.9-21.2 | 178-424 | 방어 - "근접 공격을 방어합니다 / 일정 확률로 카운터 합니다" | Shogun (sword) |
| 21.25-25.3 | 425-506 | 방어 - "창의 카운터는 바로 뒤쪽에도 공격판정이 있습니다" | Shogun (spear) |
| 25.35-29.3 | 507-586 | 방어 파괴 - "공격량을 누적시키면 방어가 파괴되고 스턴합니다" | Shogun (spear) |
| 29.35-34.9 | 587-698 | 스턴 회복 - "스턴 회복시 작은 데미지로 넉백시킵니다 / 회피가 불가능합니다" | Shogun (spear) |
| 35.0-39.1 | 700-782 | 변신 - "맞으면 더 아프지만 어렵지는 않습니다" | Shogun -> Tenma |
| 39.2-40.1 | 784-802 | 3단 콤보 (continues in v7) | Tenma |

Hard cuts (frame + minimap discontinuity): 1.05, 8.9, 15.0 (inside 방어), 21.25, 25.35, 29.35, 39.2.

## Event log

### 마가츠의 뇌안 (single eye) 0.0-1.0
- 0.0-0.9 (t0-18): one Magatsu eye floats ~1.5 b up in front of the player, ringed by a flat
  purple lightning disc (~3 b dia). HUD: "「마가츠의 뇌안」을 계속 공격해서 제거하세요".
  Player keeps hitting it. Cut at 1.05 before it breaks (caption: breaking it stuns the boss).

### 마가츠의 뇌안 2 (multi eye) 1.05-8.9
- 1.1-1.3 (t22-26): three cyan-white light pillars drop from the sky at 3 spots
  (left / centre / right, ~6-7 b apart) = eye spawn markers.
- 1.4-1.5 (t28-30): three small purple eye orbs (diamond eye glyph, own HP bar) hang ~2-3 b up.
  A faint thin purple circle is drawn on the floor around the centre eye (r ~5-6 b) -> FLOOR RING.
- 1.9-4.9 (t38-98): player hits the centre eye (Barbara/Xingqiu skill fx clutter the shot).
  The floor ring stays visible (clear at 4.6, ellipse around the centre spot).
- 5.0 (t100): centre eye breaks (white star burst). HF 5.28 (t106).
- 5.5-6.3 (t110-126): player walks away from the remaining two eyes, stays near the broken eye's spot.
- 6.3-7.5 (t126-150): a large pale-cyan translucent glow/hemisphere builds over the remaining
  eyes' area (volumetric warning, not a floor decal).
- 7.6-8.2 (t152-164): blast - violent purple lightning + dark shard explosion along the far
  side where the two surviving eyes are; reaches to ~3-4 b behind the player who is safe.
  Onsets 7.83 (t157), 8.21 (t164), HF 8.44-8.63 (t169-173).
- Spawn -> blast ~130 t (6.5 s); warning glow ~25 t before blast.

### 방어 (guard, sword) 8.9-21.2
- Stance (all segment): Shogun stands still, katana in hand, a 5-orb halo arch over her head
  (centre eye emblem + 4 small tomoe orbs) and a purple crackling ring on the floor around her
  feet (r ~1.5-2 b) = stance aura, present the whole time (not an attack telegraph).
- Melee hits on her -> gold crescent ring flash around her waist (r ~1.2 b) = parry
  (9.2-10.4, t184-208; 10.8-11.2; HF 9.26-9.54, 10.39-10.53).
- Counter A:
  - 12.0 (t240): parry ring + a black vertical line through her (tell), HF 12.04-12.35 (t241-247).
  - 12.2 (t244): pink-white 4-point star flash at her chest.
  - 12.4-12.8 (t248-256): spinning slash burst around her (sphere/arc r ~2.5-3 b).
  - 13.0-13.2 (t260-264): pink lightning bolts streak along the floor toward the player
    (line ~6-8 b long), HF 13.01-13.26 (t260-265).
  - 13.4-13.8 (t268-276): forward lunge-thrust (purple streak through the player's spot,
    ~6-8 b), HF 13.68-14.08 (t274-282). Player dodged sideways.
- Counter B (after cut at 15.0):
  - 15.8-16.0 (t316-320): parry ring + black vertical line; 16.2 (t324) star flash
    (HF 16.04-16.74, t321-335, strongest SFX of the segment).
  - 16.4-16.8 (t328-336): slash burst sphere around her; 17.4 (t348) second gold arc.
  - 18.0-18.4 (t360-368): floor lightning bolts toward player (HF 18.02-18.39).
  - 18.8-19.4 (t376-388): lunge-thrust streak toward the player; player at ~3-4 b side-steps.
- No floor telegraph for the counters; the cue is the gold ring + black line + star flash.

### 방어 (spear counter) 21.25-25.3
- 21.25-21.4 (t425-428): Shogun now holds the naginata, crouched; dark purple aura disc under her.
- 21.5-21.7 (t430-434): parry gold ring (HF 21.55-21.85, t431-437).
- 22.1-22.3 (t442-446): parry ring + black vertical line; 22.4 (t448) star flash
  (HF 22.27-22.62, t445-452).
- 22.5-22.7 (t450-454): burst sphere around her.
- 23.2-23.9 (t464-478): 360 degree spinning spear sweep - dark-purple crescent ring trail
  around her, r ~4-5 b, includes directly behind her (caption). HF 23.32-24.38 (t466-488).
- Tell (star) -> sweep ~16-20 t. No floor decal.

### 방어 파괴 (guard break -> stun) 25.35-29.3
- 25.4-25.6 (t508-512): player's charged hits; guard shatters (white-purple burst, HF 25.36-25.74).
- 26.1-26.6 (t522-532): a golden light pillar comes down on her (stun marker), HF 26.31-26.57.
- 26.9-27.1 (t538-542): white sphere flash; she stands slumped, spear upright, halo still on.
- 27.4-28.9 (t548-578): stunned, takes hits (damage numbers 1866/1794). No attacks.

### 스턴 회복 (stun recovery knock-back) 29.35-34.9
- 29.4-30.3 (t588-606): stunned boss; a glowing purple ring on the floor around her, r ~2.5-3 b
  -> FLOOR RING visible ~20 t before the burst.
- 30.45-30.6 (t609-612): white flash then a purple shockwave dome (r ~4-5 b) with dark shards;
  player (inside the ring) is knocked back. HF 30.55-30.78 (t611-616). Undodgeable per caption.
- 31.3 cut-like jump, then 31.5-33.3 (t630-666): ring visible again under her (~35 t).
- 33.4-33.5 (t668-670): flash; 33.6-34.4 (t672-688): second shockwave + crystal shards r ~4-5 b
  (HF 33.42 t669). Ground crackle lingers to ~34.8 (t696).

### 변신 (transformation into Tenma) 35.0-39.1
- 35.1-35.6 (t702-712): boss floats at the arena centre (~12-15 b away). A ring of purple
  lightning spreads across the floor from her (expanding ground ring, passes the player area).
  A pale translucent sphere edge is also seen near the camera (expanding shell).
- 35.7-35.9 (t714-718): huge white-violet lightning pillars slam down (one ~3 b right of player),
  HF 35.77-36.33 (t715-727).
- 35.95-36.3 (t719-726): purple burst/dome at the boss + bolts raining around the arena.
- 36.5-39.1 (t730-782): the puppet-arm body (Tenma) is visible behind her; at ~37 s the sky/floor
  palette shifts from teal to dark blue-violet (phase lighting change). No further hits.
- 39.2-40.1 (t784-802): cut to "3단 콤보": Tenma at ~8 b, giant arm holds the glaive horizontal;
  40.0 (t800) pink flash on the glaive (start of the combo, continues in v7).
