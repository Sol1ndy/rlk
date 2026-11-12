# A node zone: the candidate must keep sqrt(#riftCr) tenths from the zone centre (#riftCx / #riftCz).
scoreboard players operation #riftEx room = #riftCx room
scoreboard players operation #riftEz room = #riftCz room
scoreboard players operation #riftEx room -= #riftQx room
scoreboard players operation #riftEz room -= #riftQz room
scoreboard players operation #riftEx room *= #riftEx room
scoreboard players operation #riftEz room *= #riftEz room
scoreboard players operation #riftEx room += #riftEz room
execute if score #riftEx room < #riftCr room run scoreboard players set #riftBad room 1
