# Q1 stage main tick 100
function rlk:mboss/grp_new
scoreboard players operation #q1_g kn = #mbGrp mb
function rlk:boss/arlecchino/p/q1/f/cres_r15_kb3
function rlk:boss/arlecchino/p/q1/f/cres_l15_kb3
execute at @s run playsound minecraft:item.trident.throw hostile @a[tag=player] ~ ~ ~ 1 1 0.33
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
