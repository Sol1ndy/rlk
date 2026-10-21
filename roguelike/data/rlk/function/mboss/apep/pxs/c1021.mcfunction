# sink_revive: [(0, 'p1'), (6, 'burrowed'), (46, 'parked')]
execute if score @s apRigT matches 0 unless score #apPx mb matches 0 run return run function rlk:mboss/apep/px/p1
execute if score @s apRigT matches 6 unless score #apPx mb matches 3 run return run function rlk:mboss/apep/px/burrowed
execute if score @s apRigT matches 46 unless score #apPx mb matches 6 run return run function rlk:mboss/apep/px/parked
