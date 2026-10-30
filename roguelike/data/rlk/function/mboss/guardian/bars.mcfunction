# Hook bars (@s = body, every tick in intro/fight). Under-bar: guard = leading element's record progress
# (its colour; gold = guard time left before the first counted hit), chaos = timer (Pyro code 2, D22),
# groggy = time left (green), pattern = progress (gold). Sub-line and name-line glyphs: hud/*.
execute if score #gdSt mb matches 3 if score #gdGP mb matches 2 run return run function rlk:mboss/guardian/hud/bar_guard
execute if score #gdSt mb matches 4 if score #gdCP mb matches 3 run return run function rlk:mboss/guardian/hud/bar_chaos
execute if score #gdSt mb matches 5 run return run function rlk:mboss/guardian/hud/bar_groggy
execute if score #gdPat mb matches 1.. unless score #gdPNew mb matches 1 unless score #gdPRel mb matches 1 run function rlk:mboss/guardian/hud/bar_pattern
