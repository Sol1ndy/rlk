# move_strike_p3: [(0, 'p3u'), (8, 'burrowed'), (44, 'p3c'), (85, 'p3u')]
execute if score @s apRigT matches 0 unless score #apPx mb matches 1 run return run function rlk:mboss/apep/px/p3u
execute if score @s apRigT matches 8 unless score #apPx mb matches 3 run return run function rlk:mboss/apep/px/burrowed
execute if score @s apRigT matches 44 unless score #apPx mb matches 2 run return run function rlk:mboss/apep/px/p3c
execute if score @s apRigT matches 85 unless score #apPx mb matches 1 run return run function rlk:mboss/apep/px/p3u
