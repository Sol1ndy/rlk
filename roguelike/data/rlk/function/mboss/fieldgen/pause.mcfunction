# Hook pause (the fight froze: player dead / reviving / selection screen / no body). Low gravity drops by
# itself (mboss/main clears #mbLowG every tick and the module tick does not run while paused; the module
# keeps #fgLowG and asks again after the resume). The running pattern may drop what would hang (its pause).
# The kit's ground decals go (the frozen hazards keep their framework markers; the decals would run on and
# flash early), so does a kit screen flash / pop still on the title line (only while one is up: vBig, so a
# selection screen's own title is left alone); a dead or reviving player clears the kit cards itself.
scoreboard players set #fgFlash mb 0
function rlk:mboss/fieldgen/fx/tele/clear
execute if entity @a[tag=player,scores={vBig=1..}] run function rlk:mboss/fieldgen/fx/hud/flash_end
function rlk:mboss/fieldgen/p/pause_d
