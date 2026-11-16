# The pair changed: cprep, the mirror, RES, looks of the phase, badges.
execute store result storage rlk:mboss cprep.azhdaha.pair.leg int 1 run scoreboard players get #azLeg mb
execute store result storage rlk:mboss cprep.azhdaha.pair.tail int 1 run scoreboard players get #azTail mb
data modify storage rlk:mboss az.pair set from storage rlk:mboss cprep.azhdaha.pair
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/azhdaha/res/reset
execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run function rlk:boss/azhdaha/res/apply
function rlk:boss/azhdaha/look/apply
execute if score #azPh mb matches 2.. run function rlk:boss/azhdaha/arena/look_leg
execute if score #azPh mb matches 3 run function rlk:boss/azhdaha/arena/look_tail
function rlk:boss/azhdaha/arena/glyphs
scoreboard players operation #azE mb = #azLeg mb
execute if score #azPh mb matches ..1 run scoreboard players set #azE mb 5
scoreboard players operation #azET mb = #azTail mb
execute unless score #azPh mb matches 3 run scoreboard players set #azET mb 5
scoreboard players set #azHudQ mb 1
