# 화염구 발사(0.8칸/틱, 불 원소)
tp @s ~ ~ ~ ~ ~
tag @s remove rlk_cmfbh
tag @s remove rlk_cmlink
tag @s add rlk_cmp
tag @s add rlk_cmp_fb
data modify entity @s teleport_duration set value 1
scoreboard players operation @s cmD = #cmD_fb tmp
scoreboard players operation @s cmLv = #clv tmp
scoreboard players set @s cmEl 1
scoreboard players set @s cmT 40
execute unless score #k90 snd matches 1 run function rlk:snd/f97
