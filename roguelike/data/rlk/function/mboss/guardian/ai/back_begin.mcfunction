# @s = body: #gdPick wants a hop back (player nearer than its away distance): 12 t, then the pattern.
function rlk:mboss/guardian/ai/back_dest
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_gd_bk,limit=1] run return run function rlk:mboss/guardian/ai/go
scoreboard players set #gdSt mb 8
scoreboard players set #gdT mb 0
function rlk:mboss/guardian/rig/face/player
function rlk:mboss/guardian/rig/play/backstep
execute as @s positioned as @e[type=minecraft:marker,tag=rlk_mb_gd_bk,limit=1] run function rlk:mboss/mv/glide {t:11}
particle minecraft:poof ~ ~0.15 ~ 0.5 0.05 0.5 0.03 8 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:calcite"} ~ ~0.1 ~ 0.5 0.05 0.5 0 12 force @a[tag=player]
particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~0.12 ~ 0.8 0.02 0.8 0 8 force @a[tag=player]
playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.6 0.9 0.2
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.35 1.3 0.12
playsound minecraft:block.calcite.break hostile @a[tag=player] ~ ~ ~ 0.5 0.8 0.17
function rlk:mboss/guardian/hud/sub_pattern
