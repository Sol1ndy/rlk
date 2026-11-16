# As a new clone husk at its feet: face the player, hittable at once; its object display gives way to the clone
# figure (14 parts, build_raiden_clones.mjs).
tag @s add rlk_rd_illusion
tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute rotated as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rdHitCD 0
scoreboard players operation #rdIlId rd = @s rdObjId
execute as @e[type=minecraft:item_display,tag=rlk_rd_objvisual,tag=!rlk_rd_clp] if score @s rdObjId = #rdIlId rd run kill @s
execute store result storage rlk:rd il.id int 1 run scoreboard players get @s rdObjId
execute rotated as @s run function rlk:boss/raiden/clone/summon with storage rlk:rd il
