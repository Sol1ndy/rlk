# intro: the timeline at #sq 1356 (@s = the body).
function rlk:mboss/title {title:"홍련",sub:"월하곡",color:"#E8466A"}
function rlk:boss/scarlet/fx/snd/draw
function rlk:boss/scarlet/rig/anchor/blade_tip
execute at @e[type=minecraft:marker,tag=rlk_hr_anchor,limit=1] run function rlk:boss/scarlet/fx/p/glint {c:5}
execute positioned ~ ~1.1 ~ rotated as @s rotated ~ 0 run function rlk:boss/scarlet/fx/p/qi_arc {r:18,yaw:0,pitch:0,roll:0,c:1}
