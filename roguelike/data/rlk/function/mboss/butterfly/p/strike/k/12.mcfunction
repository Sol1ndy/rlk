# strike clock 12
# the ground slash band along her path (the kit wing_band arc at L + floor slashes from her spot)
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11l,limit=1] run function rlk:mboss/butterfly/fx/p/wing_band
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] positioned ^ ^0.05 ^2 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~90 90",bb:"fixed",roll:0,spin:0,s0:2.8,s1:3.2,move:"0f,0f,0f",life:8,fade:4,col:3705195}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] positioned ^ ^0.07 ^2 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~90 90",bb:"fixed",roll:0,spin:0,s0:2.5,s1:3,move:"0f,0f,0f",life:8,fade:4,col:15203754}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] positioned ^ ^0.05 ^4 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~90 90",bb:"fixed",roll:0,spin:0,s0:2.8,s1:3.2,move:"0f,0f,0f",life:8,fade:4,col:3705195}
execute at @e[type=minecraft:marker,tag=rlk_mb_bf_p11s,limit=1] positioned ^ ^0.07 ^4 run function rlk:mboss/butterfly/fx/card {kind:"streak",pos:"~ ~ ~",rot:"~90 90",bb:"fixed",roll:0,spin:0,s0:2.5,s1:3,move:"0f,0f,0f",life:8,fade:4,col:15203754}
function rlk:mboss/butterfly/wx/u/fwd {d:0.12}
