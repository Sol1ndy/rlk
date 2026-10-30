# #apPick -> the main slot (p/run starts it this tick); #apLast for the attack patterns; #apLastMv for moves.
execute if score #apPick mb matches 1 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 2 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 3 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 4 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 5 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 6 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 31 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 33 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 34 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 35 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 36 run scoreboard players operation #apLast mb = #apPick mb
execute if score #apPick mb matches 32 run scoreboard players operation #apLast mb = #apPick mb
scoreboard players set #apLastMv mb 0
execute if score #apPick mb matches 10 run scoreboard players set #apLastMv mb 1
scoreboard players operation #apPid mb = #apPick mb
scoreboard players set #apPNew mb 1
scoreboard players set #apReqT mb 0
