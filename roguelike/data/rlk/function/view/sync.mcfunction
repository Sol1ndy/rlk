# 플레이어가 순간이동한 직후에 부른다 (@s = 플레이어): 아바타도 그 자리로
execute unless entity @e[tag=rlk_av,limit=1] run return 0
execute at @s run tp @e[tag=rlk_av,limit=1] ~ ~ ~ ~ 0
data modify entity @e[tag=rlk_av,limit=1] Motion set value [0.0d,0.0d,0.0d]
execute at @s run tp @e[tag=rlk_camv,limit=1] ~ ~ ~
