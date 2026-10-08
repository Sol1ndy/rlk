# 결정 파편 표시 (@s = 플레이어): 숄더뷰(아바타가 있을 때)만. 아바타 옆, 카메라 기준 왼쪽을 따라다닌다
execute if entity @s[tag=rlk_body] run return run function rlk:char/navia/sh_clear
execute unless entity @e[tag=rlk_av,limit=1] run return run function rlk:char/navia/sh_clear
execute unless score @s nvS = @s nvShK run function rlk:char/navia/sh_build
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.45 ^1.68 ^-0.05 run tp @e[tag=rlk_nvsh,scores={nvShI=0}] ~ ~ ~ ~ 0
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.45 ^1.45 ^-0.05 run tp @e[tag=rlk_nvsh,scores={nvShI=1}] ~ ~ ~ ~ 0
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.45 ^1.22 ^-0.05 run tp @e[tag=rlk_nvsh,scores={nvShI=2}] ~ ~ ~ ~ 0
# 길어진 조각(4개 이상): 반짝이
execute store result score #t1 tmp run time query gametime
scoreboard players operation #t1 tmp %= #st4 tmp
execute if score #t1 tmp matches 0 if score @s nvS matches 4.. at @e[tag=rlk_nvsh,scores={nvShI=0}] run particle minecraft:wax_on ~ ~ ~ 0.12 0.03 0.03 0 1
execute if score #t1 tmp matches 0 if score @s nvS matches 5.. at @e[tag=rlk_nvsh,scores={nvShI=1}] run particle minecraft:wax_on ~ ~ ~ 0.12 0.03 0.03 0 1
execute if score #t1 tmp matches 0 if score @s nvS matches 6.. at @e[tag=rlk_nvsh,scores={nvShI=2}] run particle minecraft:wax_on ~ ~ ~ 0.12 0.03 0.03 0 1
