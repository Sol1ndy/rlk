$execute positioned $(x) 201 $(z) if entity @e[tag=rlk_body,distance=..5] if score #try tmp matches ..8 run return 0
$execute if block $(x) 200 $(z) #rlk:dash_pass run return 0
$execute unless block $(x) 201 $(z) #rlk:dash_pass run return 0
$execute unless block $(x) 202 $(z) #rlk:dash_pass run return 0
$execute positioned $(x) 201 $(z) run function rlk:room/mob_summon
scoreboard players set #placed tmp 1
