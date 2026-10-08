# 잔향 표시 (@s = 플레이어): 숄더뷰(아바타가 있을 때)만. 카메라 기준 왼쪽, 위에서 아래로 나갈 순서대로
execute if entity @s[tag=rlk_body] run return run kill @e[tag=rlk_rnec]
execute unless entity @e[tag=rlk_av,limit=1] run return run kill @e[tag=rlk_rnec]
scoreboard players operation #k tmp = @s rnE3
scoreboard players operation #k tmp *= #st10 tmp
scoreboard players operation #k tmp += @s rnE2
scoreboard players operation #k tmp *= #st10 tmp
scoreboard players operation #k tmp += @s rnE1
execute unless score #k tmp = @s rnEcK run function rlk:char/ronova/ec_build
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.75 ^1.58 ^-0.05 run tp @e[tag=rlk_rnec,scores={rnEcI=0}] ~ ~ ~ ~ 0
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.75 ^1.40 ^-0.05 run tp @e[tag=rlk_rnec,scores={rnEcI=1}] ~ ~ ~ ~ 0
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.75 ^1.22 ^-0.05 run tp @e[tag=rlk_rnec,scores={rnEcI=2}] ~ ~ ~ ~ 0
