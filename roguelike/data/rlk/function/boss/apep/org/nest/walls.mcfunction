# t12: the walls rise from the locked spots; flying again, the next cast 160 t later.
scoreboard players operation #apX mb = @s apL
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_wlock] if score @s apL = #apX mb at @s run function rlk:boss/apep/wall/raise
scoreboard players set @s apS 1
scoreboard players set @s apTok 160
