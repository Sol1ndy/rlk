# dash clock 11
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"burst",pos:"^ ^1.4 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:4,move:"0f,0f,0f",life:4,fade:2,col:16777215}
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"^ ^1.4 ^1.2",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1.5,s1:3.5,move:"0f,0f,0f",life:4,fade:2,col:16383456}
execute at @s rotated as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] rotated ~ 0 run particle minecraft:flash{color:[0.98,0.99,0.88,0.9]} ^ ^1.4 ^1.2 0 0 0 0 1 force @a[tag=player]
function rlk:mboss/butterfly/fx/snd/dash_kick
playsound minecraft:entity.player.attack.strong hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
