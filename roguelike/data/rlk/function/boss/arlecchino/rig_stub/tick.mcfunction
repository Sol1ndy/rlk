# Stand-in rig tick (@s = body): the shown clip tick #rigt kn; a faint column marks the body.
scoreboard players add #rigt kn 1
execute if score #rigt kn matches 0.. run particle minecraft:dust{color:[0.88,0.19,0.23],scale:1.0} ~ ~1.4 ~ 0.14 0.6 0.14 0 2 force @a[tag=player]
