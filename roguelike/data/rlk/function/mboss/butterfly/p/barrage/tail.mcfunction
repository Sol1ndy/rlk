# As / at a crescent (rlk_mb_bf_p12qy), its helper marker rlk_mb_bf_p12qx at its spot one tick ago: a flame streak 1-2 b long behind
# it, lying along its actual flight (from there to here) in the plane that holds the flight line and the level
# cross-line, so the player it dives at sees it full; the camera-facing claw is its head (review fix F4).
# Decorative: it gives way near the fx card cap (#bkN 48+; fix FX-2).
execute if score #bkN mb matches 48.. run return 0
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12qx,limit=1] at @s facing entity @e[type=minecraft:item_display,tag=rlk_mb_bf_p12qy,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute if entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12qx,distance=..0.05,limit=1] run return 0
execute store result score #bp12P mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_bf_p12qx,limit=1] Rotation[1]
execute if score #bp12P mb matches 0.. rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p12qx,limit=1] positioned ^ ^ ^-0.7 rotated ~ ~-90 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~ ~",bb:"fixed",roll:90,spin:0,s0:1.8,s1:0.7,move:"0f,0f,0f",life:3,fade:1,col:16163649}
execute if score #bp12P mb matches ..-1 rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p12qx,limit=1] positioned ^ ^ ^-0.7 rotated ~ ~90 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~ ~",bb:"fixed",roll:90,spin:0,s0:1.8,s1:0.7,move:"0f,0f,0f",life:3,fade:1,col:16163649}
