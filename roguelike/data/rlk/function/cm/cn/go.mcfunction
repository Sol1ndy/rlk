# 숨겨 둔 포탄 발사
tag @s remove rlk_cmcbw
tag @s remove rlk_cmlink
tag @s add rlk_cmp
tag @s add rlk_cmp_cb
data merge entity @s {transformation:{translation:[-0.2f,-0.2f,-0.2f],scale:[0.4f,0.4f,0.4f]}}
particle minecraft:explosion ~ ~ ~ 0 0 0 0 1
particle minecraft:large_smoke ~ ~ ~ 0.15 0.15 0.15 0.04 8
execute unless score #k93 snd matches 1 run function rlk:snd/f100
