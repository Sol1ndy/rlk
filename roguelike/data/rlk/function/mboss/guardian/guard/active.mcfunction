# @s = body, guard clock 51..150: gold aura, drift ~1 b/s toward the player, record window.
function rlk:mboss/guardian/rig/face/track
execute unless entity @e[tag=rlk_body,distance=..2.2,limit=1] run function rlk:mboss/mv/toward {d:0.05}
scoreboard players operation #gdM mb = #gdT mb
scoreboard players operation #gdM mb %= #gdK3 mb
execute if score #gdM mb matches 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:0.9} ~ ~1.9 ~ 0.55 1 0.55 0 3 force @a[tag=player]
execute if score #gdM mb matches 0 run particle minecraft:wax_on ~ ~1.6 ~ 0.8 1.2 0.8 0 1 force @a[tag=player]
execute if score #gdT mb matches 139..150 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.3} ~ ~2 ~ 0.45 0.9 0.45 0 4 force @a[tag=player]
execute if score #gdT mb matches 146 run execute rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"star",pos:"^ ^2.4 ^0.5",rot:"~ ~",bb:"center",roll:0,spin:60,s0:0.4,s1:3.2,move:"0f,0f,0f",life:8,fade:4}
execute if score #gdT mb matches 146 run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.3
execute if score #gdRecNew mb matches 1.. run return run function rlk:mboss/guardian/guard/record
execute if score #gdT mb matches 150.. run function rlk:mboss/guardian/guard/timeout
