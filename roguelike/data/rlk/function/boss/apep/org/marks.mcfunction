# AP-REV (plan 7.6.4-7.6.7, 8.2): the organism runtime.
# The stage markers (rev/ready, rev/reload; at the floor, rlk_mb_aux): the 3 cradle sockets (rlk_mb_ap_skm<i>, r 3.4 at
# [0.0, 120.0, 240.0]) and the 3 파괴 stops (rlk_mb_ap_dstop, r 2.6 at [60.0, 180.0, 300.0]) of the Heart footprint.
function rlk:boss/apep/org/marks_kill
summon minecraft:marker 440 201 4.6 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_skm","rlk_mb_ap_skm0"]}
summon minecraft:marker 442.944 201 9.7 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_skm","rlk_mb_ap_skm1"]}
summon minecraft:marker 437.056 201 9.7 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_skm","rlk_mb_ap_skm2"]}
summon minecraft:marker 442.252 201 6.7 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_dstop"]}
summon minecraft:marker 440 201 10.6 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_dstop"]}
summon minecraft:marker 437.748 201 6.7 {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_om","rlk_mb_ap_dstop"]}
