# FN-cam: camera stand $(id) (1 = rlk_mb_cam1, 2 = rlk_mb_cam2) at the execution position facing the execution rotation,
# the rotation in its summon NBT: its first frame on the client is this pose (no glide, no spin). Idempotent per stand.
$execute if entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam$(id),limit=1] run return 0
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_camr"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_camr,limit=1] run tp @s ~ ~ ~ ~ ~
execute store result storage rlk:mboss camsp.yaw float 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_camr,limit=1] Rotation[0] 1000
execute store result storage rlk:mboss camsp.pitch float 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_camr,limit=1] Rotation[1] 1000
kill @e[type=minecraft:marker,tag=rlk_mb_camr]
$data modify storage rlk:mboss camsp.id set value $(id)
function rlk:mboss/cam/spawn_in with storage rlk:mboss camsp
data remove storage rlk:mboss camsp
