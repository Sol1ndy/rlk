# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick
# after its kill at 106 (it would respawn).
execute if score #mbT mb matches 1..105 run function rlk:mboss/fieldgen/rig_stub/tick
execute if score #mbT mb matches 4..4 run function rlk:mboss/fieldgen/cfx/death_flicker
execute if score #mbT mb matches 9..9 run function rlk:mboss/fieldgen/cfx/death_flicker
execute if score #mbT mb matches 12 run function rlk:mboss/fieldgen/rig_stub/look/off
execute if score #mbT mb matches 20 run function rlk:mboss/fieldgen/cfx/death_drop
execute if score #mbT mb matches 40 run function rlk:mboss/fieldgen/cfx/death_sink
execute if score #mbT mb matches 90 run function rlk:mboss/fieldgen/cfx/death_out
execute if score #mbT mb matches 106 run function rlk:mboss/fieldgen/rig_stub/kill
