# From combat/apply after element/on_hit and combat/apply_mods (@s = aux with rlk_mb_hit; #dmg #elem #elU #rx
# #tfm #crit known). #dmg is already modified exactly like a hit on the body (engravings, items, level factor,
# Ronova, the aux's own mres), so a pool sized as a share of the boss's max HP (#auxHpPct) breaks in that share
# of the boss's kill time. The module hook may change #dmg or take over completely (#mbAuxDone mb 1); by
# default #dmg comes off the aux's mhpC with a number. Nothing here re-enters combat/apply; a broken aux gets
# rlk_mb_broken and the module acts on it in its tick.
scoreboard players set #hitLanded tmp 1
execute unless entity @s[tag=rlk_mb_broken] run function rlk:mboss/aux_hit2
# Like the end of combat/apply: a frost crit made for this target only does not spread to the next one.
execute if score #frostC eng matches 1 run scoreboard players set #crit tmp 0
execute if score #frostC eng matches 1 run scoreboard players set #frostC eng 0
