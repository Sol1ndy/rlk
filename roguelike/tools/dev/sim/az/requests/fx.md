
## Rpa-2 kit: an outline-only (no progress fill) option for tele/disc (Change note 1 "keep (trim)")
- what: Change note 1 keeps the P4 spike landing ring as "zig-zag crack ring outline 14 t before each landing ... no
  progress fill" (also the P9 rock rings, the P1 Hydro geyser swirl). `tele/disc {r, tell, el, nd, hold}` always grows the
  `t_fill` card. Asked for: a `fill` argument (0 = rim only, default 1 = today), or a `tele/rim {r, tell, el, hold}` with
  the same timing (the rim flashes at call + tell), same storage-macro interface. s2.md 18.5 item 7.
- needed by: P4 landings t32 / 37 / 40 / 45 (geo_a.py `p/spikes/land<k>`, `p/spikes/redraw<k>`); until served, geo_a
  calls `tele/disc` (rim + fill) with the hazard's own tell 14, which the tests accept (decal = hazard).
- status: open

## Rpt-3 kit: an outline-only option for the seal telegraphs (Change note 1 "keep (trim)")
- what: Change note 1 trims 41's heptagram, 45's star seals (and 32's seal8) to "outline + rune, no progress fill" and
  keeps 46's hexagram as a zone marker; `tele/heptagram|starseal|hexagram|seal8 {r, tell, el, hold}` always grow the
  `t_fill` card under the art (tele/e/seal). Asked for: a `fill` argument (0 = art + rim only, default 1 = today), same
  storage-macro interface (S2-T's resume redraws call them `with storage rlk:mboss az.tl`).
- needed by: tail.py p/frost/make (B3 70 + 34 k, tell 22), p/icespike/f0-2 (t26, tells 42 / 48 / 54), p/elspike/hex1 /
  hex_<i> and every resume; until served they are called with the hazard's own tell (the fill reaches the rim on the
  hit), which pat_tail.py accepts (decal = hazard).
- status: open

## Rpb-1 kit: the outline-only tele/disc of Rpa-2 is also the P9 rock-ring look (S2-B)
- what: P9's four rock rings (r 3.4, tell 19, Geo, Change note 1 "keep (trim)": the gold chevron ring outline, no
  progress fill) call `tele/disc {r:34,tell:19,el:5,nd:0,hold:3}` from geo_b.py `p/burrow/ring_at` and redraw it on
  resume (`p/burrow/ring_redraw`, `with storage rlk:mboss az.tl`). Served by Rpa-2's `fill` argument / `tele/rim`; a
  chevron (zig-zag) rim sprite instead of the plain `t_rim` would match v2 D / v3 A better (optional).
- needed by: geo_b.py P9 (t50 / 75 / 120 / 145); until served the rim + fill grows over the hazard's own tell 19, which
  pat_geo_b.py accepts (decal = hazard).
- status: open
