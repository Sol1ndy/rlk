# Q1 stage main tick 46
function rlk:mboss/grp_new
scoreboard players operation #q1_g kn = #mbGrp mb
execute at @s run function rlk:boss/arlecchino/fx/snd/crescent_throw
execute if score #q1_k kn matches 3 run function rlk:boss/arlecchino/p/q1/f/cres_c_kb3
execute unless score #q1_k kn matches 3 run function rlk:boss/arlecchino/p/q1/f/cres_c_kb0
