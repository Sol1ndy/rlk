# Hook intro_tick (@s = body, #mbT 1..; untargetable). Clip tick = #mbT - 1; the fight at #mbT 151.
function rlk:boss/azhdaha/rig/tick
function rlk:boss/azhdaha/seq/intro/tick
execute if score #mbT mb matches 151.. run function rlk:boss/azhdaha/intro/done
