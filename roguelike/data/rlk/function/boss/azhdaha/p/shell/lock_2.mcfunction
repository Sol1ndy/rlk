# Shell 3: the lock (the player's feet), the hazard (dive 8 t after the launch in 4 t), the cue.
function rlk:boss/azhdaha/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_az_p44l2]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p44l2
tag @e[type=minecraft:marker,tag=rlk_mb_az_p44l2] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p44l2] add rlk_mb_az_p44
tag @e[type=minecraft:marker,tag=rlk_mb_az_p44l2] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p44l2] remove rlk_mb_lock
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 441
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzGrp mb = #aq44G mb
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p44l2,limit=1] run function rlk:mboss/hz/disc {r:24,tell:12,dmg:58}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p44
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p44s2,limit=1] run particle minecraft:flash{color:[0.773f,0.545f,1f,1f]} ~ ~ ~ 0 0 0 0 1 force @a[tag=player]
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p44s2,limit=1] run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.1 8 force @a[tag=player]
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p44s2,limit=1] run playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 1 1.9 0.33
