# S5 cure fx, t 3 (at the player's body).
execute if entity @e[tag=rlk_av,limit=1] run particle minecraft:dust{color:[0.957f,0.929f,0.788f],scale:1.3} ~ ~4.5 ~ 0.05 0.5 0.05 0 6 force @a[tag=player]
execute if entity @e[tag=rlk_av,limit=1] run particle minecraft:dust{color:[1f,1f,1f],scale:0.8} ~ ~3.9 ~ 0.05 0.2 0.05 0 2 force @a[tag=player]
playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.4 2 0.13
