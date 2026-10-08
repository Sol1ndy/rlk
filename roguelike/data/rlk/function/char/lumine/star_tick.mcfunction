# @s = 혹한의 별, 실행 위치 = 플레이어. 플레이어 머리 위를 돌며 2초마다 가까운 적에게 얼음 결정
scoreboard players remove @s life 1
execute if score @s life matches ..0 run return run function rlk:char/lumine/star_end
execute rotated as @s run tp @s ^ ^2.3 ^0.9 ~7 ~
scoreboard players operation #sl tmp = @s life
scoreboard players operation #sl tmp %= #c40 tmp
execute if score #sl tmp matches 20 as @e[tag=rlk_mob,sort=nearest,limit=1,distance=..11] run function rlk:char/lumine/crystal
