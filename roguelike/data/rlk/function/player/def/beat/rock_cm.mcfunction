# @s = 커스텀 몹의 두뇌, at @s: 같은 cmId 의 모습 부품
scoreboard players operation #cid cb = @s cmId
execute as @e[type=minecraft:item_display,tag=rlk_cmlink,distance=..6] if score @s cmId = #cid cb at @s rotated ~ 0 run function rlk:player/def/beat/rock1
