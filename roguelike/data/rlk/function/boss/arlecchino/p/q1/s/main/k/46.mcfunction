# Q1 stage main tick 46
function rlk:mboss/grp_new
scoreboard players operation #q1_g kn = #mbGrp mb
execute at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
execute if score #q1_k kn matches 3 run function rlk:boss/arlecchino/p/q1/f/cres_c_kb3
execute unless score #q1_k kn matches 3 run function rlk:boss/arlecchino/p/q1/f/cres_c_kb0
