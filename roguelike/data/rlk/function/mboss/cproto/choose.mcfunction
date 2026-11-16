scoreboard players add #cpNext mb 1
execute if score #cpNext mb matches 4.. run scoreboard players set #cpNext mb 1
scoreboard players operation #cpPat mb = #cpNext mb
execute if score #mbLock mb matches 1..3 run scoreboard players operation #cpPat mb = #mbLock mb
scoreboard players set #cpT mb 0
