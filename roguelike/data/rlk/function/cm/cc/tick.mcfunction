# 우인단 번개 시킨 술사 (@s = brain, at @s). Summons 4 cicins (cap 4, a new flock only when all are dead and
# the cooldown is over), sends one at a time; blinks 6 b away from a close body (5 s), then is dazed (punish).
function rlk:cm/cc/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/cc/reset
function rlk:cm/cc/flock
execute if score @s cmS matches 1 run return run function rlk:cm/cc/c_tell
execute if score @s cmS matches 2 run return run function rlk:cm/cc/c_after
execute if score @s cmS matches 3 run return run function rlk:cm/cc/b_shim
execute if score @s cmS matches 4 run return run function rlk:cm/cc/dazed
execute if entity @e[tag=rlk_body,distance=..7] run scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd2 matches ..0 if entity @e[tag=rlk_body,distance=..3] run return run function rlk:cm/cc/b_start
execute if score #ccN tmp matches 0 if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..22] run function rlk:cm/cc/c_start
