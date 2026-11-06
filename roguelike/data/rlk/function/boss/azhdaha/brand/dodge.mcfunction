# @s = body: a perfect dodge (#mbDodgeOk 1: one-shot strike >= 12 t, not nododge, or a pj) cleanses, once per 40 t.
execute unless score #mbDodgeOk mb matches 1 run return 0
execute unless entity @a[tag=player,scores={azBrT=1..},limit=1] run return 0
scoreboard players operation #azX mb = #azClk mb
scoreboard players operation #azX mb -= #azDgClk mb
execute if score #azX mb matches ..39 run return 0
scoreboard players operation #azDgClk mb = #azClk mb
execute as @a[tag=player,scores={azBrT=1..},limit=1] run function rlk:boss/azhdaha/brand/cleanse
