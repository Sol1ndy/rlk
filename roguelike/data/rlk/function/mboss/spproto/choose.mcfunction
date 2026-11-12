scoreboard players add #spNext mb 1
execute if score #spNext mb matches 3.. run scoreboard players set #spNext mb 1
scoreboard players operation #spPat mb = #spNext mb
execute if score #mbLock mb matches 1..2 run scoreboard players operation #spPat mb = #mbLock mb
scoreboard players set #spT mb 0
