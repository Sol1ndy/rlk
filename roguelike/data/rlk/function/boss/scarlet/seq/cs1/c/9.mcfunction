# cs1: the camera at #sq 9 (@s = the body).
scoreboard players set #mbCamId mb 2
function rlk:mboss/cam/text
data merge entity @e[type=minecraft:item_display,tag=rlk_mb_cam2,limit=1] {teleport_duration:12}
