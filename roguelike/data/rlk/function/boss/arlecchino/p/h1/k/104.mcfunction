# H1 pattern tick 104
scoreboard players set #bolw kn 1
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^3.3 run particle minecraft:sweep_attack ~ ~ ~ 1.8 0.15 1.8 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^3.3 run particle minecraft:dust{color:[0.72,0.04,0.12],scale:1.6} ~ ~ ~ 1.8 0.2 1.8 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^3.3 run particle minecraft:crimson_spore ~ ~ ~ 1.5 0.2 1.5 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.5 0.33
execute at @s run playsound minecraft:entity.wither.shoot hostile @a[tag=player] ~ ~ ~ 0.4 1.4 0.13
function rlk:boss/arlecchino/rig_stub/look/glow/normal
