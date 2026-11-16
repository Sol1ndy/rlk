# 수면 포격 (surface, id 36; plan 8.3). sink 0-20 (hidden from 12), the surfacing point at 26, surface 36, shell hit 48, stand 76-90.
scoreboard players set #apq36O mb 0
execute if score @s apRigStance matches 0 run scoreboard players set #apq36O mb 14
execute if score #apq36O mb matches 14 run function rlk:boss/apep/play/stand_p3
execute if score #apq36O mb matches 14 run scoreboard players add #apPLen mb 14
scoreboard players operation #apq36T mb = #apPT mb
scoreboard players operation #apq36T mb -= #apq36O mb
kill @e[tag=rlk_mb_ap_p36]
