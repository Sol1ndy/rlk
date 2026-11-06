# kick clock 0
function rlk:mboss/butterfly/rig/face/track
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p1a,limit=1] run function rlk:mboss/mv/glide {t:5}
playsound minecraft:entity.breeze.jump hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
playsound minecraft:block.moss_carpet.step hostile @a[tag=player] ~ ~ ~ 0.5 1 0.17
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.25 1.5 0
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"leaf",pos:"^ ^0.3 ^-0.6",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.3,s1:0.4,move:"0f,-0.3f,0f",life:10,fade:4,col:11067252}
particle minecraft:poof ~ ~0.1 ~ 0.25 0.02 0.25 0.02 2 force @a[tag=player]
