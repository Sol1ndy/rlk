# Stand-in rig tick (@s = body): the shown clip tick #rigt tk; a faint column marks the body.
scoreboard players add #rigt tk 1
execute if score #rigt tk matches 0.. run particle minecraft:dust{color:[0.95,0.72,0.2],scale:1.0} ~ ~1.2 ~ 0.12 0.45 0.12 0 2 force @a[tag=player]
