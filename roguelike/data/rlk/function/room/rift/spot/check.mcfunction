# At a candidate (block centre, feet = the ground found): 1 when the rift may stand here, else fail. A 3 x 3 footprint
# of solid floor (not #rlk:no_spawn, leaves, logs; theme 4 house floors excluded as room/mob_up) at the same y with 3 b
# of #rlk:dash_pass above all nine and no water / lava; not over a pit (zone data.pits, its warning box); >= 4.5 b
# from every door, >= 3.5 b from every room object (rlk_obj, rlk_odisp, the fountain of XP), >= 5 b from the player
# (horizontal); a node zone keeps its centre clear.
execute if block ~-1 ~-1 ~-1 #rlk:dash_pass run return fail
execute unless block ~-1 ~ ~-1 #rlk:dash_pass run return fail
execute unless block ~-1 ~1 ~-1 #rlk:dash_pass run return fail
execute unless block ~-1 ~2 ~-1 #rlk:dash_pass run return fail
execute if block ~-1 ~ ~-1 minecraft:water run return fail
execute if block ~-1 ~ ~-1 minecraft:lava run return fail
execute if block ~-1 ~-1 ~-1 #rlk:no_spawn run return fail
execute if block ~-1 ~-1 ~-1 #minecraft:leaves run return fail
execute if block ~-1 ~-1 ~-1 #minecraft:logs run return fail
execute if score #th room matches 4 if block ~-1 ~-1 ~-1 minecraft:spruce_planks run return fail
execute if block ~-1 ~-1 ~ #rlk:dash_pass run return fail
execute unless block ~-1 ~ ~ #rlk:dash_pass run return fail
execute unless block ~-1 ~1 ~ #rlk:dash_pass run return fail
execute unless block ~-1 ~2 ~ #rlk:dash_pass run return fail
execute if block ~-1 ~ ~ minecraft:water run return fail
execute if block ~-1 ~ ~ minecraft:lava run return fail
execute if block ~-1 ~-1 ~ #rlk:no_spawn run return fail
execute if block ~-1 ~-1 ~ #minecraft:leaves run return fail
execute if block ~-1 ~-1 ~ #minecraft:logs run return fail
execute if score #th room matches 4 if block ~-1 ~-1 ~ minecraft:spruce_planks run return fail
execute if block ~-1 ~-1 ~1 #rlk:dash_pass run return fail
execute unless block ~-1 ~ ~1 #rlk:dash_pass run return fail
execute unless block ~-1 ~1 ~1 #rlk:dash_pass run return fail
execute unless block ~-1 ~2 ~1 #rlk:dash_pass run return fail
execute if block ~-1 ~ ~1 minecraft:water run return fail
execute if block ~-1 ~ ~1 minecraft:lava run return fail
execute if block ~-1 ~-1 ~1 #rlk:no_spawn run return fail
execute if block ~-1 ~-1 ~1 #minecraft:leaves run return fail
execute if block ~-1 ~-1 ~1 #minecraft:logs run return fail
execute if score #th room matches 4 if block ~-1 ~-1 ~1 minecraft:spruce_planks run return fail
execute if block ~ ~-1 ~-1 #rlk:dash_pass run return fail
execute unless block ~ ~ ~-1 #rlk:dash_pass run return fail
execute unless block ~ ~1 ~-1 #rlk:dash_pass run return fail
execute unless block ~ ~2 ~-1 #rlk:dash_pass run return fail
execute if block ~ ~ ~-1 minecraft:water run return fail
execute if block ~ ~ ~-1 minecraft:lava run return fail
execute if block ~ ~-1 ~-1 #rlk:no_spawn run return fail
execute if block ~ ~-1 ~-1 #minecraft:leaves run return fail
execute if block ~ ~-1 ~-1 #minecraft:logs run return fail
execute if score #th room matches 4 if block ~ ~-1 ~-1 minecraft:spruce_planks run return fail
execute if block ~ ~-1 ~ #rlk:dash_pass run return fail
execute unless block ~ ~ ~ #rlk:dash_pass run return fail
execute unless block ~ ~1 ~ #rlk:dash_pass run return fail
execute unless block ~ ~2 ~ #rlk:dash_pass run return fail
execute if block ~ ~ ~ minecraft:water run return fail
execute if block ~ ~ ~ minecraft:lava run return fail
execute if block ~ ~-1 ~ #rlk:no_spawn run return fail
execute if block ~ ~-1 ~ #minecraft:leaves run return fail
execute if block ~ ~-1 ~ #minecraft:logs run return fail
execute if score #th room matches 4 if block ~ ~-1 ~ minecraft:spruce_planks run return fail
execute if block ~ ~-1 ~1 #rlk:dash_pass run return fail
execute unless block ~ ~ ~1 #rlk:dash_pass run return fail
execute unless block ~ ~1 ~1 #rlk:dash_pass run return fail
execute unless block ~ ~2 ~1 #rlk:dash_pass run return fail
execute if block ~ ~ ~1 minecraft:water run return fail
execute if block ~ ~ ~1 minecraft:lava run return fail
execute if block ~ ~-1 ~1 #rlk:no_spawn run return fail
execute if block ~ ~-1 ~1 #minecraft:leaves run return fail
execute if block ~ ~-1 ~1 #minecraft:logs run return fail
execute if score #th room matches 4 if block ~ ~-1 ~1 minecraft:spruce_planks run return fail
execute if block ~1 ~-1 ~-1 #rlk:dash_pass run return fail
execute unless block ~1 ~ ~-1 #rlk:dash_pass run return fail
execute unless block ~1 ~1 ~-1 #rlk:dash_pass run return fail
execute unless block ~1 ~2 ~-1 #rlk:dash_pass run return fail
execute if block ~1 ~ ~-1 minecraft:water run return fail
execute if block ~1 ~ ~-1 minecraft:lava run return fail
execute if block ~1 ~-1 ~-1 #rlk:no_spawn run return fail
execute if block ~1 ~-1 ~-1 #minecraft:leaves run return fail
execute if block ~1 ~-1 ~-1 #minecraft:logs run return fail
execute if score #th room matches 4 if block ~1 ~-1 ~-1 minecraft:spruce_planks run return fail
execute if block ~1 ~-1 ~ #rlk:dash_pass run return fail
execute unless block ~1 ~ ~ #rlk:dash_pass run return fail
execute unless block ~1 ~1 ~ #rlk:dash_pass run return fail
execute unless block ~1 ~2 ~ #rlk:dash_pass run return fail
execute if block ~1 ~ ~ minecraft:water run return fail
execute if block ~1 ~ ~ minecraft:lava run return fail
execute if block ~1 ~-1 ~ #rlk:no_spawn run return fail
execute if block ~1 ~-1 ~ #minecraft:leaves run return fail
execute if block ~1 ~-1 ~ #minecraft:logs run return fail
execute if score #th room matches 4 if block ~1 ~-1 ~ minecraft:spruce_planks run return fail
execute if block ~1 ~-1 ~1 #rlk:dash_pass run return fail
execute unless block ~1 ~ ~1 #rlk:dash_pass run return fail
execute unless block ~1 ~1 ~1 #rlk:dash_pass run return fail
execute unless block ~1 ~2 ~1 #rlk:dash_pass run return fail
execute if block ~1 ~ ~1 minecraft:water run return fail
execute if block ~1 ~ ~1 minecraft:lava run return fail
execute if block ~1 ~-1 ~1 #rlk:no_spawn run return fail
execute if block ~1 ~-1 ~1 #minecraft:leaves run return fail
execute if block ~1 ~-1 ~1 #minecraft:logs run return fail
execute if score #th room matches 4 if block ~1 ~-1 ~1 minecraft:spruce_planks run return fail
execute store result score #riftPx room run data get storage rlk:room rsp.x
execute store result score #riftPz room run data get storage rlk:room rsp.z
execute unless function rlk:room/rift/spot/pits run return fail
# distances (tenths, horizontal): the candidate centre
scoreboard players operation #riftQx room = #riftPx room
scoreboard players operation #riftQx room *= #riftC10 room
scoreboard players add #riftQx room 5
scoreboard players operation #riftQz room = #riftPz room
scoreboard players operation #riftQz room *= #riftC10 room
scoreboard players add #riftQz room 5
scoreboard players set #riftBad room 0
scoreboard players set #riftRr room 2025
execute as @e[tag=rlk_door] run function rlk:room/rift/spot/far
scoreboard players set #riftRr room 1225
execute as @e[tag=rlk_obj] run function rlk:room/rift/spot/far
execute as @e[tag=rlk_odisp] run function rlk:room/rift/spot/far
execute as @e[tag=rlk_xpspot] run function rlk:room/rift/spot/far
execute as @e[tag=rlk_xpsrc] run function rlk:room/rift/spot/far
scoreboard players set #riftRr room 2500
execute as @e[tag=rlk_body] run function rlk:room/rift/spot/far
execute if score #riftBad room matches 1 run return fail
execute if score #riftCr room matches 1.. run function rlk:room/rift/spot/node
execute if score #riftBad room matches 1 run return fail
return 1
