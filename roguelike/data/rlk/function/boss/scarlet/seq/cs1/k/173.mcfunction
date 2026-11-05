# cs1 at #sq 173 (@s = the body).
execute as @e[type=minecraft:item_display,tag=rlk_hr_sqp_2,limit=1] at @e[type=minecraft:marker,tag=rlk_hr_stage,limit=1] positioned ^0 ^ ^1.6 positioned ~ 202.528 ~ facing entity @e[tag=rlk_body,limit=1] eyes run tp @s ~ ~ ~ ~ ~
scoreboard players set #hrLook hr 2
function rlk:boss/scarlet/rig/look/phase/p2
