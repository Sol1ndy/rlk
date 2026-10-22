# 70: a strike brand of the current absorbed element (phase 1: the leg element).
scoreboard players operation #azBrIn mb = #azLeg mb
execute if score #azPh mb matches 3 run scoreboard players operation #azBrIn mb = #azTail mb
scoreboard players set #azBrStrike mb 1
execute as @a[tag=player,limit=1] run function rlk:boss/azhdaha/brand/apply
