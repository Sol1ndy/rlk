# 신벌 진행 (@s = 플레이어)
scoreboard players add @s rnQ 1
execute if score @s rnQ matches 8 at @e[tag=rlk_rnq,limit=1] rotated as @e[tag=rlk_rnq,limit=1] run function rlk:char/ronova/wave {c:90,e:0}
execute if score @s rnQ matches 14 at @e[tag=rlk_rnq,limit=1] rotated as @e[tag=rlk_rnq,limit=1] run function rlk:char/ronova/wave {c:90,e:0}
execute if score @s rnQ matches 18 at @e[tag=rlk_rnq,limit=1] rotated as @e[tag=rlk_rnq,limit=1] run function rlk:char/ronova/replay_all
execute if score @s rnQ matches 19.. run function rlk:char/ronova/q_end
