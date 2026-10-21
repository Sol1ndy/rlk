# 증폭의 풀 (shells, id 33; plan 8.3). shells: ring 10, lock 1 33 -> hit 45, locks 79 / 82 -> hits 93 / 96, end 113.
scoreboard players set #apq33O mb 0
execute if score @s apRigStance matches 0 run scoreboard players set #apq33O mb 14
execute if score #apq33O mb matches 14 run function rlk:boss/apep/play/stand_p3
execute if score #apq33O mb matches 14 run scoreboard players add #apPLen mb 14
scoreboard players operation #apq33T mb = #apPT mb
scoreboard players operation #apq33T mb -= #apq33O mb
kill @e[tag=rlk_mb_ap_p33]
scoreboard players set #apq33G mb 0
