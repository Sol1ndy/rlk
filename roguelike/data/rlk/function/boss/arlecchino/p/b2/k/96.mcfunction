# B2 pattern tick 96
scoreboard players set #bolw kn 1
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run particle minecraft:explosion ~ ~ ~ 0.55 0.1 0.55 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.88 0.2 0.88 0 24 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.evoker_fangs.attack hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run playsound minecraft:entity.wither.hurt hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
function rlk:boss/arlecchino/rig_stub/look/glow/normal
