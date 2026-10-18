# burst clock 5
execute at @s run particle minecraft:flash{color:[0.98,0.87,0.66,1.0]} ~ ~6 ~ 0 0 0 0 1 force @a[tag=player]
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 1 1.2 0.33
