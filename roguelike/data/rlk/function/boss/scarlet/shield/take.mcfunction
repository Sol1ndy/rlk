# One segment goes (-10, never below 0): the shards and the crack at the player.
execute if score #gau hr matches ..0 run return 0
scoreboard players remove #gau hr 10
execute if score #gau hr matches ..-1 run scoreboard players set #gau hr 0
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/pip_break
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/fx/snd/pip_break
