# dash clock 10
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] run function rlk:mboss/mv/glide {t:2}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_bf_p3a,limit=1] feet rotated ~ 0 run function rlk:mboss/butterfly/fx/p/dash_streak
execute at @s rotated as @s rotated ~ 0 run function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"^ ^1.2 ^",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1.2,s1:0.4,move:"0f,0f,0f",life:4,fade:2,col:11729885}
function rlk:mboss/butterfly/fx/snd/dash
