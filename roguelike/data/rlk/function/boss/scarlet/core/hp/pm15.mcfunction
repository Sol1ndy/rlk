# A scripted HP step (@s = body): true damage of 15 per mille of her max HP (Electro number).
scoreboard players operation #mbTrue mb = @s mhpM
scoreboard players set #t5 hr 15
scoreboard players set #t4 hr 0
execute if score #mbTrue mb matches ..2000000 run scoreboard players set #t4 hr 1
execute if score #t4 hr matches 1 run scoreboard players operation #mbTrue mb *= #t5 hr
scoreboard players operation #mbTrue mb /= #c1000 hr
execute if score #t4 hr matches 0 run scoreboard players operation #mbTrue mb *= #t5 hr
execute if score #mbTrue mb matches ..0 run scoreboard players set #mbTrue mb 1
scoreboard players set #mbTrueEl mb 3
function rlk:mboss/true_hit
