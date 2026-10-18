# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick
# after its kill at 106 (it would respawn).
execute if score #mbT mb matches 1..105 run function rlk:mboss/fieldgen/rig_stub/tick
execute if score #mbT mb matches 12 run function rlk:mboss/fieldgen/rig_stub/look/off
function rlk:mboss/fieldgen/seq_c/death/tick
execute if score #mbT mb matches 106 run function rlk:mboss/fieldgen/rig_stub/kill
