# 1 = first visible frame (rig/tick already snapped the parts); 2 = restore 1-tick smoothing.
execute if score @s rdHidden matches 2.. as @e[tag=rlk_raiden_part] run data merge entity @s {teleport_duration:1}
execute if score @s rdHidden matches 2.. run return run scoreboard players set @s rdHidden 0
scoreboard players set @s rdHidden 2
