# As a clone at its feet: aim lock on the player, sword raised, glint card on the blade.
tp @s ~ ~ ~ facing entity @e[tag=rlk_body,limit=1] feet
execute rotated as @s run tp @s ~ ~ ~ ~ 0
function rlk:boss/raiden/illusion/pose {model:"prop/clone_ready_dark"}
execute rotated as @s positioned ^ ^2.6 ^0.3 run function rlk:boss/raiden/fx/star
