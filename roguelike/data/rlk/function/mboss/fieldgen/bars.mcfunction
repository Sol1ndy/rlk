# Hook bars (@s = body, every tick in intro/fight). Under-bar: the break meter while the field is open (violet,
# hits of 20; full during the break), groggy = time left (green), recovery = progress (green), pattern =
# progress (Geo), cruise idle = cruise patterns done toward the next field (gold). Text lines: hud/*.
execute if score #mbSt mb matches 0 run return 0
execute if score #fgOpen mb matches 1 run return run function rlk:mboss/fieldgen/hud/bar_meter
execute if score #fgSt mb matches 6 run return run function rlk:mboss/fieldgen/hud/bar_full
execute if score #fgSt mb matches 3 run return run function rlk:mboss/fieldgen/hud/bar_groggy
execute if score #fgSt mb matches 4 run return run function rlk:mboss/fieldgen/hud/bar_recover
execute if score #fgPat mb matches 1.. unless score #fgPNew mb matches 1 unless score #fgPRel mb matches 1 run return run function rlk:mboss/fieldgen/hud/bar_pattern
execute if score #fgField mb matches 0 run function rlk:mboss/fieldgen/hud/bar_next
