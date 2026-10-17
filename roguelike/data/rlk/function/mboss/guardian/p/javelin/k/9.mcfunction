# javelin clip tick 9
function rlk:mboss/guardian/rig/face/track
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^-0.8 ^0.9 ^0.9",rot:"~ 0",bb:"fixed",roll:-20,spin:60,s0:1.6,s1:2.5,move:"0f,0f,0f",life:5,fade:2}
execute at @s rotated as @s rotated ~ 0 positioned ^-2.602 ^0.483 ^2.417 run particle minecraft:dust{color:[1f,0.96f,0.75f],scale:0.9} ~ ~ ~ 0.5 0.3 0.5 0 12 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-2.602 ^0.483 ^2.417 run particle minecraft:end_rod ~ ~ ~ 0.3 0.2 0.3 0.04 5 force @a[tag=player]
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
playsound minecraft:block.amethyst_block.break hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
