# The cast blockers (only when a cast is due): a 파괴 within 6 b of the Heart (fusing ones sit at r 2.6), a 포식성
# in a bite chain (apS 6).
scoreboard players set #apDNear mb 0
scoreboard players set #apPChain mb 0
execute positioned 440 201 8 if entity @e[type=minecraft:husk,tag=rlk_mb_ap_destr,tag=!rlk_mb_ap_dying,distance=..6] run scoreboard players set #apDNear mb 1
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_pred,scores={apS=6}] run scoreboard players set #apPChain mb 1
