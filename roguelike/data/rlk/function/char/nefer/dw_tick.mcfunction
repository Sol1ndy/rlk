# 풀 이슬 표시 (@s = 플레이어): 숄더뷰만. 카메라 기준 왼쪽
execute if entity @s[tag=rlk_body] run return run kill @e[tag=rlk_nfdw]
execute unless entity @e[tag=rlk_av,limit=1] run return run kill @e[tag=rlk_nfdw]
execute unless score @s nfDew = @s nfDwK run function rlk:char/nefer/dw_build
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.75 ^1.70 ^-0.05 run tp @e[tag=rlk_nfdw,scores={nfDwI=0}] ~ ~ ~ ~ 0
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.75 ^1.42 ^-0.05 run tp @e[tag=rlk_nfdw,scores={nfDwI=1}] ~ ~ ~ ~ 0
execute at @e[tag=rlk_av,limit=1] rotated as @s rotated ~ 0 positioned ^0.75 ^1.14 ^-0.05 run tp @e[tag=rlk_nfdw,scores={nfDwI=2}] ~ ~ ~ ~ 0
