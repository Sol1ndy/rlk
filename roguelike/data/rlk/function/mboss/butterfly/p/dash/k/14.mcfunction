# dash clock 14
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"^ ^1.6 ^1.0",rot:"~ 0",bb:"fixed",roll:35,spin:0,s0:3,s1:4,move:"0f,0f,0f",life:3,fade:1,col:15793910}
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
