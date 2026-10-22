# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end). Clip tick t = intro t - 1:
# dormant, the clank (16), the pods unfold (30), the eye opens (60: nameplate), the rise
# (64..94), the fight at intro 95 (the idle turn to the player flows into the first pick).
function rlk:mboss/fieldgen/rig/tick
execute if score #mbT mb matches 61 run function rlk:mboss/fieldgen/intro/name
function rlk:mboss/fieldgen/seq_c/entrance/tick
execute if score #mbT mb matches 95..999 run function rlk:mboss/fieldgen/intro/done
