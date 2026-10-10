# Copy the already captured attack yaw; true illusion shows two crossing cuts.
execute if score @s rdReal matches 1 run function rlk:boss/raiden/object_vfx/cross
execute unless score @s rdReal matches 1 run function rlk:boss/raiden/object_vfx/slash
