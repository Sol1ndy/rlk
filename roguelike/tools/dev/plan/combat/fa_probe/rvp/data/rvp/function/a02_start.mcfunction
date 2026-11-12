kill @e[tag=rvpR]
kill @e[tag=rvpN]
kill @e[tag=rvpH]
summon minecraft:armor_stand 0.5 120 4.5 {Tags:["rvpH","rlk_body"],NoGravity:1b}
item replace entity @e[tag=rvpH,limit=1] weapon.mainhand with minecraft:stick[minecraft:custom_data={rlk_ui:{role:"attack"}}]
scoreboard players set @e[tag=rvpH] rcT 0
scoreboard players set @e[tag=rvpH] dashCool 0
scoreboard players set #dgTry cb -1000000
scoreboard players set #H_fail rvp 0
scoreboard players set #H_rcTmax rvp 0
scoreboard players set #H_dg rvp 0
scoreboard players set #H_rc rvp 0
scoreboard players set #k rvp 0
scoreboard players set #mode rvp 3
