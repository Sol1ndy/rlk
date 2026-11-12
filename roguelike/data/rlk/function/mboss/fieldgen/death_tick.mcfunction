# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick
# after its kill at 110 (it would respawn).
execute if score #mbT mb matches 1..109 run function rlk:mboss/fieldgen/rig/tick
execute if score #mbT mb matches 12 run function rlk:mboss/fieldgen/rig/look/off
function rlk:mboss/fieldgen/seq_c/death/tick
execute if score #mbT mb matches 110 run function rlk:mboss/fieldgen/rig/kill
