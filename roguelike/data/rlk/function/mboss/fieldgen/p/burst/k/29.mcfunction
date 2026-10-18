# burst clock 29
execute at @s run particle minecraft:dust{color:[0.98f,0.871f,0.659f],scale:1.6} ~ ~9 ~ 0.15 2 0.15 0 6 force @a[tag=player]
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.9 1.2 0.3
