# Hook tick (@s = body, at @s, fight state). Order: clocks and flags, the heal orbs (a pickup heals),
# heal events (any heal cures 달빛 고치), the cure fx, Burning, form clocks, AI state, pattern slot, then the
# rig (a clip played this tick starts this tick).
scoreboard players add #bfClk mb 1
execute if score #bfFlash mb matches 1 run function rlk:mboss/butterfly/rig_stub/flash
scoreboard players set #bfFlash mb 0
execute if score #bfDewN mb matches 1.. run function rlk:mboss/butterfly/dew/all
execute if score #mbHealEv mb matches 1.. run function rlk:mboss/butterfly/coc/heal_ev
execute if score #bfCureT mb matches 1.. run function rlk:mboss/butterfly/coc/cure_fx
execute if score #bfBurnQ mb matches 1 run function rlk:mboss/butterfly/burn/start
execute if score #bfTcN mb matches 1.. run function rlk:mboss/butterfly/tc/all
execute if score #bfForm mb matches 1 run scoreboard players add #bfHumT mb 1
execute if score #bfForm mb matches 2 run scoreboard players add #bfBfT mb 1
function rlk:mboss/butterfly/ai/state
execute if score #bfPat mb matches 1.. run function rlk:mboss/butterfly/p/run
function rlk:mboss/butterfly/rig_stub/tick
