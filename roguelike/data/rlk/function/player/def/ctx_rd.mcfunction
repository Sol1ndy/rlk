# @s = 나루카미의 위험 지대 표식(cm/hit_pl ← boss/raiden/hurt). 공격자 = 나루카미(보스 등급)
scoreboard players set #hcC tmp 2
execute unless score #hcK tmp matches 1.. run scoreboard players set #hcK tmp 3
tag @e[tag=rlk_raiden,limit=1] add rlk_hc_atk
