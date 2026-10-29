scoreboard players set @s cmS 5
scoreboard players set @s cmT 10
tag @s add rlk_c2_busy
function rlk:cm/ch_begin
execute facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
tag @s add rlk_c2_fix
playsound minecraft:item.crossbow.loading_start master @a ~ ~ ~ 1 0.6
playsound minecraft:entity.spider.ambient master @a ~ ~ ~ 0.8 0.7
