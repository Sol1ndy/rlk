# 달빛 고치 cure fx clock #bfCureT 1..20 at the player's body: gold beam down (1-6), gold burst with a ring (7-11),
# gold emblem with sparkles (12-20).
execute at @e[tag=rlk_body,limit=1] run function rlk:mboss/butterfly/coc/cure_at
scoreboard players add #bfCureT mb 1
execute if score #bfCureT mb matches 21.. run scoreboard players set #bfCureT mb 0
