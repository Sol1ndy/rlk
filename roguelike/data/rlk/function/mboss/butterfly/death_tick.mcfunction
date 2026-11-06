# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick
# after its kill at 100 (it would respawn).
execute if score #mbT mb matches 1..99 run function rlk:mboss/butterfly/rig/tick
execute if score #mbT mb matches 100 run function rlk:mboss/butterfly/rig/kill
function rlk:mboss/butterfly/seq_h/death/tick
