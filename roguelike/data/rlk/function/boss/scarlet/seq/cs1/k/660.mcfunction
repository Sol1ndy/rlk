# cs1: the timeline at #sq 660 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_3,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^-0.96 ^0.908 ^3.34 facing entity @e[type=minecraft:armor_stand,tag=rlk_mb_cam2,limit=1] feet run tp @s ~ ~ ~ ~ ~
scoreboard players set #hrLook hr 2
function rlk:boss/scarlet/rig/look/phase/p2
