# Hook pause (the fight froze: player dead / reviving / selection screen / no body). Low gravity drops by
# itself (mboss/main clears #mbLowG every tick and the module tick does not run while paused; the module
# keeps #fgLowG and asks again after the resume). The running pattern may drop what would hang (its pause).
scoreboard players set #fgFlash mb 0
function rlk:mboss/fieldgen/p/pause_d
