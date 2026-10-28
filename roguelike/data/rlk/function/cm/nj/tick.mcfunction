# 그림자 닌자 (@s = brain, at @s). Vanish in smoke -> reappear behind the body on safe ground -> 0.6 s glint
# -> slash. After two ambushes: 1.5 s exhausted (punish). Far away: a three-shuriken fan after a 0.5 s tell.
function rlk:cm/nj/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/nj/reset
execute if entity @e[tag=rlk_nj_shu,limit=1] run function rlk:cm/nj/shu_all
execute if score @s cmS matches 1 run return run function rlk:cm/nj/v_out
execute if score @s cmS matches 2 run return run function rlk:cm/nj/v_tell
execute if score @s cmS matches 3 run return run function rlk:cm/nj/v_after
execute if score @s cmS matches 4 run return run function rlk:cm/nj/tired
execute if score @s cmS matches 5 run return run function rlk:cm/nj/s_tell
execute if score @s cmS matches 6 run return run function rlk:cm/nj/s_after
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd2 matches ..0 unless entity @e[tag=rlk_body,distance=..10] if entity @e[tag=rlk_body,distance=..24] run return run function rlk:cm/nj/s_start
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..10] run function rlk:cm/nj/v_start
