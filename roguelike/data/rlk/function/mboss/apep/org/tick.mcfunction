# STUB (AP-CORE, ap_contract 1.6): the organism runtime; AP-REV replaces this file.
# @s = an organism husk, at it (rev/tick, phase 2): a kill pays the progress and removes it; else its clock, the
# display follows, the kind's behaviour (apK).
execute if entity @s[tag=rlk_mb_broken] run return run function rlk:mboss/apep/org/broke
scoreboard players add @s apT 1
scoreboard players operation #apO mb = @s apOI
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_om] if score @s apOI = #apO mb run tp @s ~ ~0.8 ~
execute if score @s apK matches 1 run return run function rlk:mboss/apep/org/k_basic
execute if score @s apK matches 2 run return run function rlk:mboss/apep/org/k_nurt
execute if score @s apK matches 5 run return run function rlk:mboss/apep/org/k_destr
