# rdTime 0, as the boss where the previous move left her. Leftovers go silently. She scatters where she stands
# (the release blink art) and stays hidden.
function rlk:boss/raiden/illusion/reset
function rlk:boss/raiden/object/clear
scoreboard players set @s rdBlink 0
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/rig/state/hidden
execute at @s run function rlk:boss/raiden/movement/depart
function rlk:boss/raiden/line/pohyeong
