$execute positioned $(x) $(y) $(z) if entity @e[tag=rlk_body,distance=..5] if score #try tmp matches ..8 run return 0
$execute positioned $(x) $(y) $(z) if block ~ ~-1 ~ #rlk:dash_pass run return 0
scoreboard players set #mu tmp 0
$execute positioned $(x) $(y) $(z) run function rlk:room/mob_up
