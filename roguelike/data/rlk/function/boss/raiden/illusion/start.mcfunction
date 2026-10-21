# rdTime 0, as the boss where the previous move left her. Leftovers go silently.
function rlk:boss/raiden/illusion/reset
function rlk:boss/raiden/object/clear
scoreboard players set @s rdBlink 0
kill @e[tag=rlk_rd_blink_dest]
function rlk:boss/raiden/rig/play/blink_out
execute at @s run function rlk:boss/raiden/fx/blink_out
function rlk:boss/raiden/line/pohyeong
