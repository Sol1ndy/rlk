kill @e[tag=rvpS]
kill @e[tag=rvpH]
summon minecraft:armor_stand 0.5 120 2.5 {Tags:["rvpS"],NoGravity:1b}
$scoreboard players set #per rvp $(p)
scoreboard players set #k rvp 0
scoreboard players set @e[tag=rvpS] rvpAcc 0
scoreboard players set #parWs cb 0
scoreboard players set #parMl cb -1000000
scoreboard players set #mode rvp 2
