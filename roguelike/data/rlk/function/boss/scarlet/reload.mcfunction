# Hook reload (@s = body after /reload: the rig parts, hazards, markers, props and kit cards are gone; scores are kept).
# PLAN §3.8: intro -> its end; CS1 -> SQ1 tick 0; SQ1 / a lead-in -> restarted from 0 (crimson first); a gauntlet -> as
# pause (lead_stand {g}); CS2 / CS3 -> their end (the rest of the HP steps); down -> on with <= 100 t; a P1 / P2 pattern
# -> cancelled + the recovery. (The death state never gets here: the framework finishes it at once.)
function rlk:boss/scarlet/init
function rlk:boss/scarlet/rig/init
function rlk:boss/scarlet/rig/spawn
scoreboard players set #lock hr 0
function rlk:boss/scarlet/core/deco_re
execute if score #ph hr matches 0 run return run function rlk:boss/scarlet/core/intro/reload
execute if score #ph hr matches 11 run return 0
function rlk:boss/scarlet/core/looks
execute if score #rp hr matches 1 run function rlk:boss/scarlet/core/replay/end
execute if score #ph hr matches 1 if score #pat hr matches 1.. run function rlk:boss/scarlet/core/cancel_pat
execute if score #ph hr matches 7 if score #pat hr matches 1.. run function rlk:boss/scarlet/core/cancel_pat
execute if score #ph hr matches 2.. run function rlk:boss/scarlet/core/re/look
execute if score #ph hr matches 2 run return run function rlk:boss/scarlet/core/re/cs1
execute if score #ph hr matches 3 run return run function rlk:boss/scarlet/core/re/lead60
execute if score #ph hr matches 4 run return run function rlk:boss/scarlet/core/re/g
execute if score #ph hr matches 9 run return run function rlk:boss/scarlet/core/re/g
execute if score #ph hr matches 5 run return run function rlk:boss/scarlet/core/re/repel
execute if score #ph hr matches 10 run return run function rlk:boss/scarlet/core/re/repel
execute if score #ph hr matches 6 run return run function rlk:boss/scarlet/core/re/down
execute if score #ph hr matches 8 run return run function rlk:boss/scarlet/core/re/lead
