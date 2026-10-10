# A short tangential step between selected patterns, with the actual walk clip.
scoreboard players set @s rdWalk 12
execute store result score @s rdWalkDir run random value 0..1
scoreboard players set @s rdAnim 1
