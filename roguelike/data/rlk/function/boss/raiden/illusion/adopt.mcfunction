# As the new hitbox husk; execution rotation = its running direction.
tag @s add rlk_rd_illusion
tp @s ~ ~ ~ ~ 0
scoreboard players set @s rdTurns 0
# Untouchable while the four overlap and run; hittable once they hold their spots.
scoreboard players set @s rdHitCD 100
scoreboard players operation #rdIlId rd = @s rdObjId
execute as @e[type=minecraft:item_display,tag=rlk_rd_objvisual] if score @s rdObjId = #rdIlId rd run function rlk:boss/raiden/illusion/adopt_visual
