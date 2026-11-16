# @s = a 양육: links up to 3 basics within r 10 (nurt_buff tell 20 t, tethers from 8); NURTURE_MODE A: immune itself (rlk_mb_ap_imm + the cylinder) while it holds >= 1 link (apSock = the links).
execute if score #apClk8 mb matches 0 if score @s apSock matches 1.. run function rlk:boss/apep/org/nurt/tethers
execute if score #apClk40 mb matches 0 if score @s apSock matches 1.. at @s run function rlk:boss/apep/fx/snd/o5_hum
execute if score @s apS matches 2 run return run function rlk:boss/apep/org/nurt/cast
scoreboard players remove @s apTok 1
execute if score @s apTok matches 1.. run return 0
execute if score @s apSock matches 3.. run return run scoreboard players set @s apTok 20
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_buff,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,distance=..10] run return run function rlk:boss/apep/org/nurt/cast_go
scoreboard players set @s apTok 20
