# Q3 stage cut tick 46
function rlk:mboss/grp_new
scoreboard players operation #q3_g kn = #mbGrp mb
execute at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
function rlk:boss/arlecchino/p/q3/f/cres_c_kb3
