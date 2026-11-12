# 성수 붉은 독수리 (@s = NoAI flying brain, at @s). Circles the body ~3 b up inside the room box. Dive: rise + shriek
# 0.5 s -> aim 0.7 s (shadow line on the ground, locked for the last 0.3 s, path checked clear) -> straight dive 18 pyro
# -> crashed 1.5 s (punish) -> takes off. Fan: wings spread 0.6 s -> 5 burning feathers +-30 deg (7 pyro each).
function rlk:cm/rv/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/rv/reset
execute as @e[tag=rlk_rv_tgt] if score @s cmId = #cid tmp run tag @s add rlk_cmsync
execute if entity @e[tag=rlk_rv_fe,limit=1] run function rlk:cm/rv/fe_all
execute if score @s cmS matches 1 run return run function rlk:cm/rv/d_rise
execute if score @s cmS matches 2 run return run function rlk:cm/rv/d_aim
execute if score @s cmS matches 3 run return run function rlk:cm/rv/dive
execute if score @s cmS matches 4 run return run function rlk:cm/rv/grounded
execute if score @s cmS matches 5 run return run function rlk:cm/rv/takeoff
execute if score @s cmS matches 6 run return run function rlk:cm/rv/f_tell
execute if score @s cmS matches 7 run return run function rlk:cm/rv/f_rec
function rlk:cm/rv/fly
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance=3.5..13] if function rlk:cm/rv/d_try run return 0
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=5..14] run function rlk:cm/rv/f_start
