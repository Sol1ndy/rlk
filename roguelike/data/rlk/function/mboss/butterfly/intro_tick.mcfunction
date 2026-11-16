# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end). The entrance clip has
# its tick t at intro tick t + 1: cocoon over a glowing floor disc, nameplate chime (57), glow ramp
# (61), whiteout (71), burst into crystal shards (79), the drop, landing (90), she stands
# (106); the fight at intro 108. No damage.
function rlk:mboss/butterfly/rig/tick
execute if score #mbT mb matches 58 run function rlk:mboss/butterfly/intro/name
execute if score #mbT mb matches 80 run function rlk:mboss/butterfly/intro/burst
function rlk:mboss/butterfly/seq_h/entrance/tick
execute if score #mbT mb matches 108..999 run function rlk:mboss/butterfly/intro/done
