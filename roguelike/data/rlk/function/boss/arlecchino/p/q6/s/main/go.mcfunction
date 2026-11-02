# Q6 stage main: tick 0 (@s = body), clip q6.
scoreboard players set #q6_s kn 1
scoreboard players set #q6_c kn 0
function rlk:boss/arlecchino/rig_stub/play/q6
function rlk:mboss/mv/face
execute positioned as @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~0 213 ~-10 run function rlk:mboss/mv/glide {t:20}
execute at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.3 ~ run particle minecraft:crimson_spore ~ ~ ~ 0.6 0.3 0.6 0.05 20 force @a[tag=player]
