# 지원 포격 중 (@s = 플레이어, at 몸): #nvQGap 틱마다 주변 12칸 안의 적 하나에게
scoreboard players remove @s nvQ 1
scoreboard players add @s nvQT 1
execute if score @s nvQT < #nvQGap tmp run return 0
scoreboard players set @s nvQT 0
execute as @e[tag=rlk_mob,distance=..12,sort=random,limit=1] at @s run function rlk:char/navia/q_shot
