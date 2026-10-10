execute if score #dpsOn lob matches 1 if score #dpsIdle lob matches 61.. run scoreboard players set #dpsOn lob 0
execute unless score #dpsOn lob matches 1 run scoreboard players set #dpsSum lob 0
execute unless score #dpsOn lob matches 1 run scoreboard players set #dpsT lob 1
scoreboard players set #dpsOn lob 1
scoreboard players set #dpsIdle lob 0
scoreboard players operation #dpsSum lob += #dd lob
