# @s = a door / object / the player: #riftBad room 1 when it is closer (horizontal) than sqrt(#riftRr) tenths.
execute store result score #riftEx room run data get entity @s Pos[0] 10
execute store result score #riftEz room run data get entity @s Pos[2] 10
scoreboard players operation #riftEx room -= #riftQx room
scoreboard players operation #riftEz room -= #riftQz room
scoreboard players operation #riftEx room *= #riftEx room
scoreboard players operation #riftEz room *= #riftEz room
scoreboard players operation #riftEx room += #riftEz room
execute if score #riftEx room < #riftRr room run scoreboard players set #riftBad room 1
