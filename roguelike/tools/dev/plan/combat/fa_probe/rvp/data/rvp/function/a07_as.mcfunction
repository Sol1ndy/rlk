execute store result storage rvp:log a07.has_stamps int 1 if score @s parHit matches -2147483648..
function rlk:player/def/dodge_stamp
execute store result storage rvp:log a07.dgAt0 int 1 run scoreboard players get @s dgAt
execute store result storage rvp:log a07.now int 1 run time query gametime
scoreboard players set #hcC tmp 0
scoreboard players set #hcK tmp 1
scoreboard players set #hcNP tmp 0
scoreboard players set #hcND tmp 0
scoreboard players set #dodged tmp 0
function rlk:player/def/judge
execute store result storage rvp:log a07.dodged int 1 run scoreboard players get #dodged tmp
execute store result storage rvp:log a07.pdg int 1 run scoreboard players get #pdg tmp
execute store result storage rvp:log a07.dgAt1 int 1 run scoreboard players get @s dgAt
execute store result storage rvp:log a07.dgKill int 1 run scoreboard players get #dgKill cb
execute store result storage rvp:log a07.box0 int 1 if entity @e[tag=rlk_dgo]
