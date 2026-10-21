# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# @s = a broken organism (rlk_mb_broken from aux/take): the progress (+325 basic / +1400 others), the
# energy particles, removed.
execute if score @s apK matches 1 run function rlk:mboss/apep/heart/add {v:325}
execute unless score @s apK matches 1 run function rlk:mboss/apep/heart/add {v:1400}
particle minecraft:happy_villager ~ ~1 ~ 0.4 0.4 0.4 0 12 force @a[tag=player]
function rlk:mboss/apep/org/remove
