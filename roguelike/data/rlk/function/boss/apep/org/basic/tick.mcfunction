# @s = a basic husk, at it (once per tick): a new break pays and starts dying; the clock; the model clip step
# (om/basic/tick, RORG-3); dying / emerging; the state machine.
execute if entity @s[tag=rlk_mb_broken] unless entity @s[tag=rlk_mb_ap_dying] run function rlk:boss/apep/org/broke
scoreboard players add @s apT 1
function rlk:boss/apep/om/basic/tick
execute if entity @s[tag=rlk_mb_ap_dying] run return run function rlk:boss/apep/org/dying
execute if score @s apS matches 0 run return run function rlk:boss/apep/org/emerge
function rlk:boss/apep/org/basic/run
