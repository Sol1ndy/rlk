# A pip goes (@s = the window, closed now): one segment of the under bar, the shards and the crack at the player.
kill @s
execute if score #pips hr matches ..0 run return 0
scoreboard players remove #pips hr 1
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.4 0.5 0.4 0.1 14 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.1 ~ run particle minecraft:end_rod ~ ~ ~ 0.3 0.4 0.3 0.06 6 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.amethyst_cluster.break hostile @a[tag=player] ~ ~ ~ 0.8 1.4 0.27
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.attack.crit hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
