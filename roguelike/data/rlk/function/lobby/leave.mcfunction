# 지금 있던 로비 방을 떠남 (@s = 플레이어)
execute if score @s lobRoom matches 2 run function rlk:lobby/tut/cleanup
# 체험 방을 떠나면 더미를 없앤다
execute if score @s lobRoom matches 4 run kill @e[tag=rlk_dummy,tag=!rlk_tutE]
tag @e[tag=rlk_lhover] remove rlk_lhover
scoreboard players set @s lobRoom 0
