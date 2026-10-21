# #mbLock = N (test/lock): that pattern only, in its own phase (another phase's id idles); 0 unlocks.
execute if score #mbLock mb matches 1 if score #apPh mb matches 1 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 2 if score #apPh mb matches 1 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 3 if score #apPh mb matches 1 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 4 if score #apPh mb matches 1 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 5 if score #apPh mb matches 1 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 6 if score #apPh mb matches 1 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 31 if score #apPh mb matches 3 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 33 if score #apPh mb matches 3 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 34 if score #apPh mb matches 3 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 35 if score #apPh mb matches 3 run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 36 if score #apPh mb matches None run return run function rlk:mboss/apep/ai/lock_go
execute if score #mbLock mb matches 32 if score #apPh mb matches 3 run return run function rlk:mboss/apep/ai/lock_go
scoreboard players set #apCool mb 20
