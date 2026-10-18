# kick clock 40
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/fx/p/kick_axe
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"^ ^0.08 ^2.0",rot:"~ 90",bb:"fixed",roll:0,spin:0,s0:1,s1:4,move:"0f,0f,0f",life:5,fade:2,col:16777215}
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 run particle minecraft:flash{color:[0.93,0.98,0.85,0.9]} ^ ^0.5 ^2.0 0 0 0 0 1 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run function rlk:mboss/butterfly/fx/p/ground_wave
function rlk:mboss/butterfly/fx/snd/kick_impact
playsound minecraft:block.big_dripleaf.break hostile @a[tag=player] ~ ~ ~ 0.6 1 0.2
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust{color:[0.161f,0.447f,0.447f],scale:1.4} ^ ^0.2 ^1 0.3 0.1 0.3 0 3 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust_color_transition{from_color:[0.898f,0.984f,0.784f],to_color:[0.161f,0.447f,0.447f],scale:1.2} ^ ^0.3 ^1 0.3 0.2 0.3 0 4 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust{color:[0.161f,0.447f,0.447f],scale:1.4} ^ ^0.2 ^2 0.3 0.1 0.3 0 3 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] rotated ~ 0 positioned ~ 201 ~ run particle minecraft:dust_color_transition{from_color:[0.898f,0.984f,0.784f],to_color:[0.161f,0.447f,0.447f],scale:1.2} ^ ^0.3 ^2 0.3 0.2 0.3 0 4 force @a[tag=player]
