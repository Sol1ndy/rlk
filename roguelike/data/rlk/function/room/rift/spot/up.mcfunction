scoreboard players add #riftU room 1
execute if score #riftU room matches 7.. run return 0
execute unless block ~ ~ ~ #rlk:dash_pass positioned ~ ~1 ~ run return run function rlk:room/rift/spot/up
execute if function rlk:room/rift/spot/check run function rlk:room/rift/spot/accept {way:1}
