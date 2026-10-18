# Hook bars (@s = body, every tick in intro/fight). Under-bar: groggy = time left (green), turn + re-form =
# progress (green), pattern = progress (its element colour), idle butterfly = time left of the butterfly form
# (Dendro), idle human (first stretch) = time left before the transformation (gold). Text lines: hud/*.
execute if score #mbSt mb matches 0 run return 0
execute if score #bfSt mb matches 3 run return run function rlk:mboss/butterfly/hud/bar_groggy
execute if score #bfSt mb matches 4 run return run function rlk:mboss/butterfly/hud/bar_recover
execute if score #bfPat mb matches 1.. unless score #bfPNew mb matches 1 unless score #bfPRel mb matches 1 run return run function rlk:mboss/butterfly/hud/bar_pattern
execute if score #bfForm mb matches 2 run return run function rlk:mboss/butterfly/hud/bar_bform
execute if score #bfHumTL mb matches 1.. run function rlk:mboss/butterfly/hud/bar_hform
