# Hook reload (@s = body after /reload: the rig parts, hazards, markers, props and kit cards are gone; scores are kept).
# hr_design §3.6: CS0 -> its end; CS1 -> its end state -> lead60 from 0; a lead-in -> restarted from 0; a gauntlet -> as
# pause (lead_re {g}); the repel -> its end (the rest of the HP steps, then P2 / the kill); a P1 / P2 pattern ->
# cancelled + the recovery. (The death state never gets here: the framework finishes it at once.)
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
execute if score @s grgT matches 1.. run function rlk:boss/scarlet/core/grog_re
execute if score #ph hr matches 2.. run function rlk:boss/scarlet/core/re/look
execute if score #ph hr matches 2 run return run function rlk:boss/scarlet/core/re/cs1
execute if score #ph hr matches 3 run return run function rlk:boss/scarlet/core/re/lead
execute if score #ph hr matches 4 run return run function rlk:boss/scarlet/core/re/g
execute if score #ph hr matches 9 run return run function rlk:boss/scarlet/core/re/g
execute if score #ph hr matches 5 run return run function rlk:boss/scarlet/core/re/repel
execute if score #ph hr matches 10 run return run function rlk:boss/scarlet/core/re/repel
execute if score #ph hr matches 8 run return run function rlk:boss/scarlet/core/re/lead
