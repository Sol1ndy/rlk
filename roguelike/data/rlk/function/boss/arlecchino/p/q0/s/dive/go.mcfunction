# Q0 stage dive: tick 0 (@s = body), clip q0_dive.
scoreboard players set #q0_s kn 2
scoreboard players set #q0_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q0_dive
function rlk:boss/arlecchino/core/lockp
function rlk:boss/arlecchino/core/lock_short
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute positioned as @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run function rlk:mboss/mv/glide {t:20}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 0.3 0.8 0.3 0 20 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
