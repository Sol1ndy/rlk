# javelin clip tick 26
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"burst",pos:"^-0.9 ^1.5 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:25,s0:0.8,s1:2.4,move:"0f,0f,0f",life:5,fade:2}
execute at @s rotated as @s rotated ~ 0 run function rlk:fx/nv/card {kind:"glow",pos:"^-0.9 ^1.5 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:2.8,move:"0f,0f,0f",life:6,fade:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] run function rlk:fx/nv/card {kind:"ring",pos:"^ ^ ^0.2",rot:"~ ~",bb:"fixed",roll:0,spin:60,s0:1,s1:2,move:"0f,0f,0f",life:8,fade:3}
execute at @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_gd_p2a,limit=1] run function rlk:fx/nv/card {kind:"glow",pos:"^ ^ ^0.25",rot:"~ ~",bb:"fixed",roll:0,spin:0,s0:0.8,s1:1.8,move:"0f,0f,0f",life:6,fade:3}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.2 16 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:dust{color:[1f,1f,0.99f],scale:1.6} ~ ~ ~ 0.6 0.6 0.6 0 18 force @a[tag=player]
function rlk:mboss/guardian/voice/attack
playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.firework_rocket.blast hostile @a[tag=player] ~ ~ ~ 0.9 1.2 0.3
