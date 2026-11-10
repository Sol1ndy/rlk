# keep the cooldowns from running out during the groggy: casters that start while stunned (ar fm im cn) need cmCd 0
execute unless score @s cmCd matches 10.. run scoreboard players set @s cmCd 10
execute unless score @s cmCd2 matches 10.. run scoreboard players set @s cmCd2 10
