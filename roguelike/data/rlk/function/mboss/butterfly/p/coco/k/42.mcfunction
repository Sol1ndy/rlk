# coco clock 42
function rlk:mboss/butterfly/rig/face/track
execute if entity @e[tag=rlk_body,distance=..5,limit=1] run function rlk:mboss/butterfly/wx/u/away {d:0.2}
# the ball opens: a pale lime ring flash
kill @e[type=minecraft:item_display,tag=rlk_mb_bf_prop_pod]
execute rotated as @s rotated ~ 0 positioned ^ ^3.0 ^ run function rlk:mboss/butterfly/fx/card {kind:"ripple",pos:"~ ~ ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:2,s1:4,move:"0f,0f,0f",life:4,fade:2,col:13431708}
playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.5 1.5 0.17
