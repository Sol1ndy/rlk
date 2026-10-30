# Hook bars (@s = body): under-bar = progress of the running pattern (gold); the sub-line is set by choose.
execute unless score #prPat mb matches 1.. run return 0
scoreboard players operation #buSub bu = #prT mb
scoreboard players operation #buSubMax bu = #prLen mb
scoreboard players set #buSubCol bu 8
