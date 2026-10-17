# Into the pattern slot: p/run starts it this tick (pattern clock 0 = clip tick 0).
scoreboard players set #gdSt mb 1
scoreboard players operation #gdPat mb = #gdPick mb
execute if score #gdPick mb matches 4 run scoreboard players set #gdP4N mb 1
scoreboard players set #gdPNew mb 1
