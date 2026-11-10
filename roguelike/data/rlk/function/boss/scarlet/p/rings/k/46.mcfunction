# RINGS pattern tick 46
execute if score #ph hr matches 7 run function rlk:mboss/mv/turn {max:10}
execute if score #ph hr matches 7 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
