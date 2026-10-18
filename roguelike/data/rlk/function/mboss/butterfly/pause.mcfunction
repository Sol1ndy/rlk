# Hook pause (the fight froze: player dead / reviving / selection screen / no body). Death ends 달빛 고치 and
# 달빛 축복 받음 (plan "cleared on death"); the running pattern may drop what would hang (its optional pause).
# The kit's ground decals go (the frozen hazards keep their framework markers; the decals would run on and
# flash early), so does a kit screen flash / pop still on the title line (only while one is up: vBig, so a
# selection screen's own title is left alone); a dead or reviving player clears the kit cards.
scoreboard players set #bfFlash mb 0
function rlk:mboss/butterfly/fx/tele/clear
execute if entity @a[tag=player,scores={vBig=1..}] run function rlk:mboss/butterfly/fx/hud/flash_end
execute if entity @a[tag=player,scores={dead=1}] run function rlk:mboss/butterfly/coc/clear_hud
execute if entity @a[tag=player,scores={rnDie=1..}] run function rlk:mboss/butterfly/coc/clear_hud
function rlk:mboss/butterfly/p/pause_d
