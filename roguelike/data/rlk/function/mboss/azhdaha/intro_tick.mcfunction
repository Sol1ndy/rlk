# Hook intro_tick (@s = body, #mbT 1..; untargetable). Clip tick = #mbT - 1; the fight at #mbT 151.
function rlk:mboss/azhdaha/rig/tick
function rlk:mboss/azhdaha/rig_stub/chain
function rlk:mboss/azhdaha/seq/intro/tick
execute if score #mbT mb matches 151.. run function rlk:mboss/azhdaha/intro/done
