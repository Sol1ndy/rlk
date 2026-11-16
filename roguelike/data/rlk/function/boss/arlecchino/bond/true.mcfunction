# True damage of #t3 per mille (@s = body): the shock burst = mhpM x per mille, clamped so mhpC stays >= the floor + 1 (true damage
# ignores floors: the break never skips E70 / T and never kills).
scoreboard players operation #t kn = @s mhpM
execute if score #t kn matches 10000000.. run scoreboard players operation #t kn /= #c1000 kn
scoreboard players operation #t kn *= #t3 kn
execute if score @s mhpM matches ..9999999 run scoreboard players operation #t kn /= #c1000 kn
scoreboard players operation #t2 kn = @s mhpC
scoreboard players operation #t2 kn -= #mbFloor mb
scoreboard players remove #t2 kn 1
execute if score #mbFloor mb matches ..0 run scoreboard players operation #t2 kn = @s mhpC
execute if score #mbFloor mb matches ..0 run scoreboard players remove #t2 kn 1
scoreboard players operation #t kn < #t2 kn
execute if score #t kn matches ..0 run return 0
scoreboard players operation #mbTrue mb = #t kn
scoreboard players set #mbTrueEl mb 1
function rlk:mboss/true_hit
