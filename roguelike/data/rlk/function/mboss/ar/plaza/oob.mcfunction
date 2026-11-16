# @s = rlk_body (avatar or first-person player), at @s. Inside = between y 198 and 217 (wall 201..207,
# barrier cap above it; the volume box is taken at the body's own x/z) and within 22.5 blocks of the axis.
execute if entity @s[y=198,dy=19] positioned 200 ~ 8 if entity @s[distance=..22.5] run return 0
execute as @a[tag=player,limit=1] run function rlk:mboss/tp_start with storage rlk:mboss cur.start
execute as @a[tag=player,limit=1] run function rlk:view/sync
function rlk:mboss/safe_start with storage rlk:mboss cur.start
title @a[tag=player] actionbar [{text:"[중간보스] ",color:"#E0703A",bold:true},{text:"경기장 밖으로 벗어나 처음 자리로 돌아왔습니다",color:"#FFB0A0",bold:false}]
