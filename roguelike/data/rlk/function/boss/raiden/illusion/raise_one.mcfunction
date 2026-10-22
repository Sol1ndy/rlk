# As a clone husk at its feet: aim lock on the player (the figure turns with it), the glint on the raised blade.
tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute rotated as @s run tp @s ~ ~ ~ ~ 0
scoreboard players operation #rdIlId rd = @s rdObjId
execute rotated as @s as @e[type=minecraft:item_display,tag=rlk_rd_ilvis] if score @s rdObjId = #rdIlId rd run tp @s ~ ~ ~ ~ 0
execute rotated as @s positioned ^ ^3.2 ^0.3 run function rlk:boss/raiden/fx/star
