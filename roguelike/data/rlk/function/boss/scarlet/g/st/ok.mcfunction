# Round X (x_brief ruling 2): 1 while the station marker's floor point passes core/cam_ok against the live player (the
# body clause: 1.6 b off the avatar; the camera line); fail when it is gone or does not.
execute at @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] positioned ~ 201 ~ if function rlk:boss/scarlet/core/cam_ok run return 1
return fail
