# @s = the boss: she reappears floating at the centre, facing the player.
execute at @e[tag=rlk_raiden_arena,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute at @s rotated as @s run tp @s ~ ~ ~ ~ 0
execute at @s run function rlk:boss/raiden/fx/blink_in
scoreboard players operation @s rdRigL = @s rdAnim
function rlk:boss/raiden/rig/start/t_reform
