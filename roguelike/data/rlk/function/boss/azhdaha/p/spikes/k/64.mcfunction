# spikes #azPT 64
function rlk:boss/azhdaha/p/spikes/blast
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.8 1.3 0.27
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run particle minecraft:dust{color:[255f,196f,64f],scale:1.6} ~ ~1.1 ~ 0.25 0.7 0.25 0 4 force @a[tag=player]
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p4s] run particle minecraft:wax_on ~ ~1.2 ~ 0.3 0.6 0.3 0 2 force @a[tag=player]
