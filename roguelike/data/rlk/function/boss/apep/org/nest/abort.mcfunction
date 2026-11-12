# @s = a 둥지 whose cast was cut (pause): its lock gone, flying, re-cast later.
scoreboard players operation #apX mb = @s apL
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wlock] if score @s apL = #apX mb run kill @s
scoreboard players set @s apS 1
scoreboard players set @s apTok 60
function rlk:boss/apep/om/nest/play/nest_fly
