# Core service 30 (s2.md 6): the host of a leg special. Transition 2 with live orbs: roar_low + p/orbs/refresh
# (full life, no new orbs); else roar_rear and the cast slot (cast/leg at its t0, #azCT = the roar_rear tick).
scoreboard players set #azCH mb 0
execute if score #azCastFirst mb matches 1 if score #azLeg mb matches 2 if score #azBgL mb matches 31 run scoreboard players set #azCH mb 1
execute if score #azCH mb matches 1 run function rlk:boss/azhdaha/rig/play/roar_low
execute if score #azCH mb matches 1 run function rlk:boss/azhdaha/p/orbs/refresh
execute if score #azCH mb matches 0 run function rlk:boss/azhdaha/rig/play/roar_rear
execute if score #azCH mb matches 0 run function rlk:boss/azhdaha/cast/leg
