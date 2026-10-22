# As the boss: on the real clone's spot (or where she is without one), facing the player; the rig shows again.
execute as @e[tag=rlk_rd_illusion,scores={rdReal=1},limit=1] at @s run tp @e[tag=rlk_raiden,limit=1] ~ ~ ~
execute at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/vanish
function rlk:boss/raiden/rig/play/blink_in
execute at @s run function rlk:boss/raiden/movement/arrive
scoreboard players set #rdIlStep rd 3
