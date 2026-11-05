# Stand-in rig tick (@s = body): the shown clip tick #rigt hr; a faint column marks the body.
scoreboard players add #rigt hr 1
execute if score #rigt hr matches 0.. run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~1.4 ~ 0.14 0.6 0.14 0 2 force @a[tag=player]
