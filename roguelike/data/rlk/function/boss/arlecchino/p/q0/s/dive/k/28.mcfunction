# Q0 stage dive tick 28
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 3.5 0.6 3.5 0 80 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ 201 ~ run particle minecraft:crimson_spore ~ ~ ~ 3 0.4 3 0.03 30 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:block.pointed_dripstone.fall hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
function rlk:boss/arlecchino/rig_stub/look/glow/normal
