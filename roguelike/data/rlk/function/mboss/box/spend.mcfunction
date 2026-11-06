# From lvup/act/resolve (@s = player) when a mid-boss pick is used: an mbSet was chosen (or skipped) while pkMb >= 1,
# just before pkMb -1. Exactly one opened box goes: the oldest (highest oarg; box/gone). None opened (the room with
# the opened box was left and its pick stayed pending for Shift+F): nothing. Closed boxes are never removed here.
scoreboard players set #mbBoxA mb 0
execute as @e[type=minecraft:marker,tag=rlk_obj,tag=rlk_mb_boxopen] run scoreboard players operation #mbBoxA mb > @s oarg
execute as @e[type=minecraft:marker,tag=rlk_obj,tag=rlk_mb_boxopen] if score @s oarg = #mbBoxA mb at @s run return run function rlk:mboss/box/gone
