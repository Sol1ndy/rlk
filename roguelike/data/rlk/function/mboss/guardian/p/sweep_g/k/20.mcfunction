# sweep_g clip tick 20
function rlk:mboss/guardian/p/sweep_g/s0
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^1.0 ^",rot:"~-135 0",bb:"fixed",roll:180,spin:155,s0:9.6,s1:10.2,move:"0f,0f,0f",life:6,fade:2}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"crescent",pos:"^ ^0.55 ^",rot:"~-120 0",bb:"fixed",roll:180,spin:140,s0:8.2,s1:8.8,move:"0f,0f,0f",life:7,fade:3}
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.35 1.2 0.12
