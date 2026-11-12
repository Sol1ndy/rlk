# From rlk:uninstall: every rift entity and the rift objectives (the #rift* fake players go with room).
kill @e[tag=rlk_rift_part]
kill @e[tag=rlk_rift]
tag @e[tag=rlk_riftz] remove rlk_riftz
tag @e[tag=rlk_riftq] remove rlk_riftq
scoreboard objectives remove riftS
scoreboard objectives remove riftT
scoreboard objectives remove riftCd
scoreboard objectives remove riftDw
scoreboard objectives remove riftPk
scoreboard objectives remove riftA
scoreboard objectives remove riftX
scoreboard objectives remove riftY
scoreboard objectives remove riftZ
scoreboard players reset #riftOn room
scoreboard players reset #riftForce room
scoreboard players reset #riftUsed room
