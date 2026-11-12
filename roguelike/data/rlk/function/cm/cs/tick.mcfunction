# 성수 전갈 (@s = brain, at @s; cm/tick hook). Burrow: dig 0.5 s -> sand trail toward the body (untargetable) ->
# trail stops, mound shakes 0.6 s -> erupts there (uppercut 18) -> stuck 1.2 s (punish). Close: pincer 0.5 s -> 10 + 12.
# Mid range: tail charge 0.8 s (aim locks for the last 0.3 s) -> electro stab 20 along a short line.
function rlk:cm/cs/lib/pre
execute if score @s cmS matches 0 if entity @s[tag=rlk_c2_busy] run function rlk:cm/cs/reset
execute if score @s cmS matches 1 run return run function rlk:cm/cs/dig
execute if score @s cmS matches 2 run return run function rlk:cm/cs/under
execute if score @s cmS matches 3 run return run function rlk:cm/cs/mound
execute if score @s cmS matches 4 run return run function rlk:cm/cs/stuck
execute if score @s cmS matches 5 run return run function rlk:cm/cs/p_tell
execute if score @s cmS matches 6 run return run function rlk:cm/cs/p_mid
execute if score @s cmS matches 7 run return run function rlk:cm/cs/p_rec
execute if score @s cmS matches 8 run return run function rlk:cm/cs/t_tell
execute if score @s cmS matches 9 run return run function rlk:cm/cs/t_rec
execute if entity @e[tag=rlk_body,distance=..2.3] run scoreboard players set #hold tmp 1
execute if score #free tmp matches 0 run return 0
execute if score @s cmCd2 matches ..0 unless entity @e[tag=rlk_body,distance=..5.5] if entity @e[tag=rlk_body,distance=..28] run return run function rlk:cm/cs/b_start
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..2.7] run return run function rlk:cm/cs/p_start
execute if score @s cmCd matches ..0 if entity @e[tag=rlk_body,distance=..4.6] run function rlk:cm/cs/t_start
