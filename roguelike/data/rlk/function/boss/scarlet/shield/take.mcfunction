# A pip goes (@s = the window, closed now): one segment of the under bar, the shards and the crack at the player.
kill @s
execute if score #pips hr matches ..0 run return 0
scoreboard players remove #pips hr 1
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/pip_break
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/fx/snd/pip_break
