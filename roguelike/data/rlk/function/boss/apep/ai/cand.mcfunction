# @s = body: candidate weights #apC<id> in the current phase and column; gates, cooldowns, first_after, no
# immediate repeat.
scoreboard players set #apC1 mb 0
execute if score #apPh mb matches 1 if score #apCol mb matches 1 run scoreboard players set #apC1 mb 1
execute if score #apPh mb matches 1 if score #apCol mb matches 2 run scoreboard players set #apC1 mb 3
execute if score #apPh mb matches 1 if score #apCol mb matches 3 run scoreboard players set #apC1 mb 4
execute if score #apPh mb matches 1 if score #apCol mb matches 4 run scoreboard players set #apC1 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 5 run scoreboard players set #apC1 mb 2
execute if score #apFc mb < #apCdE1 mb run scoreboard players set #apC1 mb 0
execute if score #apLast mb matches 1 run scoreboard players set #apC1 mb 0
scoreboard players set #apC2 mb 0
execute if score #apPh mb matches 1 if score #apCol mb matches 1 run scoreboard players set #apC2 mb 1
execute if score #apPh mb matches 1 if score #apCol mb matches 2 run scoreboard players set #apC2 mb 3
execute if score #apPh mb matches 1 if score #apCol mb matches 3 run scoreboard players set #apC2 mb 3
execute if score #apPh mb matches 1 if score #apCol mb matches 4 run scoreboard players set #apC2 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 5 run scoreboard players set #apC2 mb 2
execute if score #apLast mb matches 2 run scoreboard players set #apC2 mb 0
scoreboard players set #apC3 mb 0
execute if score #apPh mb matches 1 if score #apCol mb matches 1 run scoreboard players set #apC3 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 2 run scoreboard players set #apC3 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 3 run scoreboard players set #apC3 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 4 run scoreboard players set #apC3 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 5 run scoreboard players set #apC3 mb 2
execute if score #apFc mb < #apCdE3 mb run scoreboard players set #apC3 mb 0
execute if score #apPatN mb matches ..2 run scoreboard players set #apC3 mb 0
execute if score #apLast mb matches 3 run scoreboard players set #apC3 mb 0
scoreboard players set #apC4 mb 0
execute if score #apPh mb matches 1 if score #apCol mb matches 1 run scoreboard players set #apC4 mb 4
execute if score #apPh mb matches 1 if score #apCol mb matches 2 run scoreboard players set #apC4 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 3 run scoreboard players set #apC4 mb 2
execute if score #apPh mb matches 1 if score #apCol mb matches 4 run scoreboard players set #apC4 mb 4
execute if score #apPh mb matches 1 if score #apCol mb matches 5 run scoreboard players set #apC4 mb 2
execute if score #apLast mb matches 4 run scoreboard players set #apC4 mb 0
scoreboard players set #apC5 mb 0
execute if score #apPh mb matches 1 if score #apCol mb matches 4 run scoreboard players set #apC5 mb 1
execute unless score #apZone mb matches 2 run scoreboard players set #apC5 mb 0
execute if score #apF mb matches 0.. run scoreboard players set #apC5 mb 0
execute if score #apFc mb < #apCdE5 mb run scoreboard players set #apC5 mb 0
execute if score #apLast mb matches 5 run scoreboard players set #apC5 mb 0
scoreboard players set #apC6 mb 0
execute if score #apPh mb matches 1 if score #apCol mb matches 1 run scoreboard players set #apC6 mb 4
execute if score #apPh mb matches 1 if score #apCol mb matches 2 run scoreboard players set #apC6 mb 1
execute if score #apPh mb matches 1 if score #apCol mb matches 4 run scoreboard players set #apC6 mb 1
execute if score #apLast mb matches 6 run scoreboard players set #apC6 mb 0
scoreboard players set #apC31 mb 0
execute if score #apPh mb matches 3 if score #apCol mb matches 1 run scoreboard players set #apC31 mb 1
execute if score #apPh mb matches 3 if score #apCol mb matches 2 run scoreboard players set #apC31 mb 2
execute if score #apPh mb matches 3 if score #apCol mb matches 3 run scoreboard players set #apC31 mb 3
execute if score #apLast mb matches 31 run scoreboard players set #apC31 mb 0
scoreboard players set #apC33 mb 0
execute if score #apPh mb matches 3 if score #apCol mb matches 1 run scoreboard players set #apC33 mb 1
execute if score #apPh mb matches 3 if score #apCol mb matches 2 run scoreboard players set #apC33 mb 3
execute if score #apPh mb matches 3 if score #apCol mb matches 3 run scoreboard players set #apC33 mb 3
execute if score #apLast mb matches 33 run scoreboard players set #apC33 mb 0
scoreboard players set #apC34 mb 0
execute if score #apPh mb matches 3 if score #apCol mb matches 1 run scoreboard players set #apC34 mb 3
execute if score #apPh mb matches 3 if score #apCol mb matches 2 run scoreboard players set #apC34 mb 2
execute if score #apPh mb matches 3 if score #apCol mb matches 3 run scoreboard players set #apC34 mb 1
execute if score #apLast mb matches 34 run scoreboard players set #apC34 mb 0
scoreboard players set #apC35 mb 0
execute if score #apPh mb matches 3 if score #apCol mb matches 1 run scoreboard players set #apC35 mb 2
execute if score #apPh mb matches 3 if score #apCol mb matches 2 run scoreboard players set #apC35 mb 2
execute if score #apPh mb matches 3 if score #apCol mb matches 3 run scoreboard players set #apC35 mb 2
execute if score #apLast mb matches 35 run scoreboard players set #apC35 mb 0
scoreboard players set #apCn mb 0
scoreboard players operation #apCn mb += #apC1 mb
scoreboard players operation #apCn mb += #apC2 mb
scoreboard players operation #apCn mb += #apC3 mb
scoreboard players operation #apCn mb += #apC4 mb
scoreboard players operation #apCn mb += #apC5 mb
scoreboard players operation #apCn mb += #apC6 mb
scoreboard players operation #apCn mb += #apC31 mb
scoreboard players operation #apCn mb += #apC33 mb
scoreboard players operation #apCn mb += #apC34 mb
scoreboard players operation #apCn mb += #apC35 mb
