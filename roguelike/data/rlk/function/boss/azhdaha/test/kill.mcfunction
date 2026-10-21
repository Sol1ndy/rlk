# 24: the death through a lethal true hit (bypasses the floor) -> the chapter clear.
execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end
scoreboard players operation #mbTrue mb = @s mhpC
scoreboard players set #mbTrueEl mb 5
function rlk:mboss/true_hit
