# As a new clone husk at its feet: face the player, hittable at once; its display becomes the posed clone.
tag @s add rlk_rd_illusion
tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute rotated as @s run tp @s ~ ~ ~ ~ 0
scoreboard players set @s rdHitCD 0
scoreboard players operation #rdIlId rd = @s rdObjId
execute rotated as @s as @e[type=minecraft:item_display,tag=rlk_rd_objvisual] if score @s rdObjId = #rdIlId rd positioned as @s run function rlk:boss/raiden/illusion/adopt_visual
