# The links (the cap tilted, the tethers from now): the nearest free basics within r 10, up to 3 links in all.
scoreboard players operation #apX mb = @s apL
scoreboard players set #apY mb 3
scoreboard players operation #apY mb -= @s apSock
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_buff,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,tag=!rlk_mb_ap_prey,distance=..10,sort=nearest,limit=3] run function rlk:boss/apep/org/nurt/link1
scoreboard players set #apZ mb 3
scoreboard players operation #apZ mb -= #apY mb
scoreboard players operation @s apSock = #apZ mb
function rlk:boss/apep/org/nurt/imm
