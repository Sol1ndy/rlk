# FN-cam (round W): the dialogue line and the hint on the LIVE camera only (#mbCamId mb 2 = rlk_mb_cam2, else
# rlk_mb_cam1: the rule of mboss/cam/hold). The texts are billboards riding their camera, 0.3 b before the eye of whoever
# looks THROUGH it; the idle camera stands somewhere in the world (prepared for the next cut, or left at the last
# shot's place), and a text on it showed small and far away in the picture. mboss_lib.cam_line / cam_hint store the
# component in storage rlk:mboss camtx and call this; a module calls it again at every cut (the other camera goes live).
execute unless score #mbCamId mb matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camx2] run data merge entity @s {text:"",background:0}
execute unless score #mbCamId mb matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camt,tag=rlk_mb_camx1] run data modify entity @s {} merge from storage rlk:mboss camtx.line
execute unless score #mbCamId mb matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camk,tag=rlk_mb_camx1] run data modify entity @s {} merge from storage rlk:mboss camtx.hint
execute if score #mbCamId mb matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camx1] run data merge entity @s {text:"",background:0}
execute if score #mbCamId mb matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camt,tag=rlk_mb_camx2] run data modify entity @s {} merge from storage rlk:mboss camtx.line
execute if score #mbCamId mb matches 2 as @e[type=minecraft:text_display,tag=rlk_mb_camk,tag=rlk_mb_camx2] run data modify entity @s {} merge from storage rlk:mboss camtx.hint
