# FN-cam: camera $(id) (1 = rlk_mb_cam1, 2 = rlk_mb_cam2) for the viewpoint at the execution position looking along the
# execution rotation: a one-tick marker takes the pose, mboss/cam/grid puts its rotation on the grid and moves it 4
# blocks forward, the camera is summoned there with that rotation in its NBT (its first frame on the client is this
# pose). Idempotent per camera.
$execute if entity @e[type=minecraft:item_display,tag=rlk_mb_cam$(id),limit=1] run return 0
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_camr"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_camr,limit=1] run tp @s ~ ~ ~ ~ ~
execute as @e[type=minecraft:marker,tag=rlk_mb_camr,limit=1] run function rlk:mboss/cam/grid
execute store result storage rlk:mboss camsp.yaw float 1.40625 run scoreboard players get #mbCamY mb
execute store result storage rlk:mboss camsp.pitch float 1.40625 run scoreboard players get #mbCamP mb
$data modify storage rlk:mboss camsp.id set value $(id)
execute at @e[type=minecraft:marker,tag=rlk_mb_camr,limit=1] run function rlk:mboss/cam/spawn_in with storage rlk:mboss camsp
kill @e[type=minecraft:marker,tag=rlk_mb_camr]
data remove storage rlk:mboss camsp
