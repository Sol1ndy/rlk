data modify entity @s transformation.scale[0] set value 0.11f
data modify entity @s transformation.scale[1] set value 0.11f
data modify entity @s transformation.translation set value [-0.055f,-0.055f,0f]
data modify entity @s block_state set value {id:"minecraft:redstone_block"}
execute at @s unless score #k106 snd matches 1 run function rlk:snd/f113
