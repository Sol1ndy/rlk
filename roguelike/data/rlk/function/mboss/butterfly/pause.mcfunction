# Hook pause (the fight froze: player dead / reviving / selection screen / no body). Death ends 달빛 고치 and
# 달빛 축복 받음 (plan "cleared on death"); the running pattern may drop what would hang (its optional pause).
scoreboard players set #bfFlash mb 0
function rlk:mboss/butterfly/tc/clear
execute if entity @a[tag=player,scores={dead=1}] run function rlk:mboss/butterfly/coc/clear_hud
execute if entity @a[tag=player,scores={rnDie=1..}] run function rlk:mboss/butterfly/coc/clear_hud
function rlk:mboss/butterfly/p/pause_d
