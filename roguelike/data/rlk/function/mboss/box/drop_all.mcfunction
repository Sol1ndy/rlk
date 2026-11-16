# From mboss/reward (@s = zone marker, at @s; #mbPk mb = cur.picks >= 1) and from the rift collapse of a killed
# special boss (room/rift/close_end: @s = the rift anchor, at it; #mbPk = its stored picks, Tachy S1). The row stands
# across the line from the drop spot to the player, its yaw snapped to the room axes, so the player sees the boxes
# side by side.
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_boxq"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_boxq,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute store result score #mbBoxY mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_boxq,limit=1] Rotation[0]
kill @e[type=minecraft:marker,tag=rlk_mb_boxq]
# quarter = (yaw + 225) / 90 mod 4: 0 player to the north (yaw 180), 1 east (-90), 2 south (0), 3 west (90)
scoreboard players add #mbBoxY mb 225
scoreboard players set #mbBoxQ mb 90
scoreboard players operation #mbBoxY mb /= #mbBoxQ mb
scoreboard players operation #mbBoxY mb %= #c4 mb
execute if score #mbPk mb matches 4.. run scoreboard players set #mbPk mb 3
scoreboard players set #mbBoxW mb 0
execute if score #mbBoxY mb matches 0 rotated 180 0 run function rlk:mboss/box/row
execute if score #mbBoxY mb matches 1 rotated -90 0 run function rlk:mboss/box/row
execute if score #mbBoxY mb matches 2 rotated 0 0 run function rlk:mboss/box/row
execute if score #mbBoxY mb matches 3 rotated 90 0 run function rlk:mboss/box/row
scoreboard players set #mbBoxOn mb 1
playsound minecraft:block.amethyst_block.chime block @a[tag=player] ~ ~6 ~ 1 1.3
playsound minecraft:entity.firework_rocket.twinkle_far block @a[tag=player] ~ ~6 ~ 0.5 1.4
