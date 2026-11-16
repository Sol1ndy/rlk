# sweep start -> landing (one hit per dash), then move there; the rig slides over 2 ticks
execute as @e[tag=rlk_kr_dst] if score @s cmId = #cid tmp run tag @s add rlk_kr_dsel
scoreboard players operation #wN tmp = @s cmD
scoreboard players set #c2h tmp 0
execute unless entity @e[tag=rlk_kr_dsel,limit=1] run scoreboard players set #wN tmp 0
execute unless entity @e[tag=rlk_kr_dsel,limit=1] run function rlk:cm/kr/a_ray
execute if entity @e[tag=rlk_kr_dsel,limit=1] facing entity @e[tag=rlk_kr_dsel,limit=1] feet run function rlk:cm/kr/a_ray
execute if score #c2h tmp matches 1 run function rlk:cm/kr/a_hit
execute if entity @e[tag=rlk_kr_dsel,limit=1] run tp @s @e[tag=rlk_kr_dsel,limit=1]
kill @e[tag=rlk_kr_dsel]
scoreboard players add @s cmN 1
scoreboard players set @s cmS 2
scoreboard players set @s cmT 2
playsound minecraft:item.trident.riptide_1 master @a ~ ~ ~ 0.9 1.5
