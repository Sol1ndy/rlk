# Arlecchino S5 review findings (wip/ar f98f38b)

- AR-00 blocker, fixed: spawn used mboss/body (miniboss tag) -> chapter reward broken; now mboss/cb/body.
- AR-01 major, fixed: wisps and intro flee target inside the rim posts; now theme POINTS['wisps'].
- AR-02 major, fixed: balance with FN-1 live far over target (P1 1.62x, P2 2.40x, worst 40 t 93 %).
- AR-03 major, fixed: counter unreachable without a healer; bond/force now resets her part to 18 % (player's own bond kept). Lead: KEEP.
- AR-04 major, fixed: Q5B final scaled with the bond; per-mille FN-1 branch no longer x #mbBolRe; final 300 permille.
- AR-05/06 minor, fixed: R-S4-1 TID keyed on first word; R-S4-2 test 45 via #q4_t3.
- AR-07 minor, fixed: H1 wing and sweep are two hits; dead wings-off key removed.
- AR-08 minor, fixed (K2): four vertical slashes use pivot 2.0; nothing below the floor.
- AR-09 minor, fixed: fx_slash double yaw offset (latent).
- AR-10 minor, fixed: cleanup leaves no kit followers or storage rlk:kn p2.
- AR-11 minor, fixed: DASH_LEN q2 20.
- AR-12 minor, fixed: README section brought up to date.
- AR-13 minor, left: airborne time (Q6 160 t, Q4 70-170 t, Q0 <=80 t, H1 perch 54 t, E1 70 t); telegraphed, hittable.
- AR-14 minor, left: one-tick spikes (G1 field 6.7 k, crimson look 4.9 k); averages fine.
- AR-15 minor, left (design): Q5B melee counter hard; ranged normal shots can counter.
- AR-16 minor, left: 289 trailing-point ticks, none on a striking frame.

Balance after: P1 1.15x Apep P1; P2 walk+orbs 1.00x Apep P3; worst 40 t 42.9 %; no-heal walker survives two Banquets.
Gates: regen x2 identical, rplint 0, atlas 12.63 M, loadcheck ar_rev 0, all AR suites green, other bosses' suites unchanged.
