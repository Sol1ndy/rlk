# @s = rlk_body, at @s. Inside = feet in y 198..237 (the volume box taken at the body's own x/z) and within
# 29.5 b of the axis of az_cavern; else back to the arrival spot.
execute if entity @s[y=198,dy=39] positioned 320 ~ 8 if entity @s[distance=..29.5] run return 0
execute as @a[tag=player,limit=1] run function rlk:mboss/ar/az_cavern/tp_in
title @a[tag=player] actionbar {text:"경기장 밖으로 벗어나 처음 자리로 돌아왔습니다",color:"#FFB0A0",bold:false}
