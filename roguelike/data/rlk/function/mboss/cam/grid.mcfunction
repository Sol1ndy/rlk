# FN-cam (@s = a camera or a helper marker standing AT a viewpoint, aimed): its rotation onto the grid the client gets
# (360 / 256 = 1.40625 degrees, the nearest step: half a step is added, the byte index floored and written back
# exactly), then 4 blocks forward along that rotation: a spectator in F5 sees a non-living camera entity from
# 4 blocks behind it (Camera.alignWithEntity), so the picture is the viewpoint's. #mbCamY / #mbCamP mb = the bytes.
execute at @s run tp @s ~ ~ ~ ~0.703125 ~0.703125
execute store result score #mbCamY mb run data get entity @s Rotation[0] 0.71111112
execute store result score #mbCamP mb run data get entity @s Rotation[1] 0.71111112
execute store result entity @s Rotation[0] float 1.40625 run scoreboard players get #mbCamY mb
execute store result entity @s Rotation[1] float 1.40625 run scoreboard players get #mbCamP mb
execute at @s run tp @s ^ ^ ^4
