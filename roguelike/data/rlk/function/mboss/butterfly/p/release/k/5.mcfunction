# release clock 5
function rlk:mboss/butterfly/rig/face/track
# the swoop past the player to R (9 t), the dive whoosh
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_bf_p15r,limit=1] run function rlk:mboss/mv/glide {t:9}
function rlk:mboss/butterfly/fx/snd/wing_dive
execute rotated as @s rotated ~ 0 positioned ~ ~0.06 ~ run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~90 90",bb:"fixed",roll:0,spin:0,s0:2,s1:3,move:"0f,0f,0f",life:4,fade:2,col:11985754}
particle minecraft:cherry_leaves ~ ~0.6 ~ 0.6 0.2 0.6 0 2 force @a[tag=player]
