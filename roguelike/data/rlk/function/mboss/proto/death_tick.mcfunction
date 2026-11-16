# Hook death_tick (@s = body, #mbT = 1.. until cur.death).
function rlk:mboss/proto/rig/follow
execute if score #mbT mb matches 20 run function rlk:mboss/proto/pose/sink {d:18}
execute if score #mbT mb matches 20.. run particle minecraft:smoke ~ ~0.6 ~ 0.4 0.3 0.4 0.01 4 force @a[tag=player]
