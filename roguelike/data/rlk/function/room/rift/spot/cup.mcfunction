scoreboard players add #riftU room 1
execute if score #riftU room matches 7.. run return 0
execute unless block ~ ~ ~ #rlk:dash_pass positioned ~ ~1 ~ run return run function rlk:room/rift/spot/cup
execute unless block ~ ~1 ~ #rlk:dash_pass run return 0
execute if block ~ ~-1 ~ #rlk:dash_pass run return 0
function rlk:room/rift/spot/accept {way:2}
