# 원시 정령 기계·재구성자 (@s = brain, at @s). Scatter into cubes 0.4 s -> reform beside the body (0.5 s cube glow at
# the spot, walked from the body) -> hammer slam r 2.5 (0.7 s raised arm + ring, 18) or cube spin r 3 (0.8 s, 14).
# After two reforms: overheated 1.5 s, core exposed (rlk_c3_core: x1.5 damage taken), stunnable.
function rlk:cm/pc/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/pc/reset
execute if score @s cmS matches 1 run return run function rlk:cm/pc/scatter
execute if score @s cmS matches 2 run return run function rlk:cm/pc/reform
execute if score @s cmS matches 3 run return run function rlk:cm/pc/sl_tell
execute if score @s cmS matches 4 run return run function rlk:cm/pc/after
execute if score @s cmS matches 5 run return run function rlk:cm/pc/sp_tell
execute if score @s cmS matches 6 run return run function rlk:cm/pc/after
execute if score @s cmS matches 7 run return run function rlk:cm/pc/overheat
execute if entity @e[tag=rlk_body,distance=..2.0] run scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..14] run function rlk:cm/pc/s_start
