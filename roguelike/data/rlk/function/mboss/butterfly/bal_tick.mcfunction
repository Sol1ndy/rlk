# @s = body, instead of the hook tick while groggy: clocks, flash, dews / cure / heal events / Burning, the rig.
scoreboard players add #bfClk mb 1
execute if score #bfFlash mb matches 1 run function rlk:mboss/butterfly/rig/flash
scoreboard players set #bfFlash mb 0
execute if score #bfDewN mb matches 1.. run function rlk:mboss/butterfly/dew/all
execute if score #bpS5T mb matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:mboss/butterfly/wx/cure/tick
execute if score #mbHealEv mb matches 1.. run function rlk:mboss/butterfly/coc/heal_ev
execute if score #bfBurnQ mb matches 1 run function rlk:mboss/butterfly/burn/start
function rlk:mboss/butterfly/rig/tick
