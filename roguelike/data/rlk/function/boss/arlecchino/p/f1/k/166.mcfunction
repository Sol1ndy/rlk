# F1 pattern tick 166
function rlk:boss/arlecchino/rig_stub/look/wings/open
execute at @s positioned ~ ~1 ~ run function rlk:mboss/mv/glide {t:6}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.4 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.2 1 1.2 0 30 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.flap hostile @a[tag=player] ~ ~ ~ 0.8 0.6 0.27
execute at @s run playsound minecraft:item.elytra.flying hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] positioned ~ 201.1 ~ run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 11.7 0.02 11.7 0 160 force @a[tag=player]
