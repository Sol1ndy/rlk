# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end). Clip tick t = intro t - 1:
# dormant, the clank (16), the pods unfold (28), the eye opens (54: nameplate), the rise
# (80..110), the fight at intro 111 (the idle turn to the player flows into the first pick).
function rlk:mboss/fieldgen/rig_stub/tick
execute if score #mbT mb matches 55 run function rlk:mboss/fieldgen/intro/name
function rlk:mboss/fieldgen/seq_c/entrance/tick
execute if score #mbT mb matches 111..999 run function rlk:mboss/fieldgen/intro/done
