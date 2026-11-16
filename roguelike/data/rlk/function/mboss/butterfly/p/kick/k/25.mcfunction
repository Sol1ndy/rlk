# kick clock 25
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p1b,limit=1] run function rlk:mboss/mv/glide {t:4}
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^ ^1.0 ^-1",rot:"~90 0",bb:"fixed",roll:0,spin:0,s0:3,s1:3.5,move:"0f,0f,0f",life:4,fade:2,col:14153881}
playsound minecraft:entity.breeze.jump hostile @a[tag=player] ~ ~ ~ 0.6 1.1 0.2
