# The shields: every solid basic within r 10 without one (the orb flares; o3_cast).
execute at @s run function rlk:boss/apep/fx/snd/o3_cast
execute as @e[type=minecraft:husk,tag=rlk_mb_ap_basic,tag=!rlk_mb_ap_shd,tag=!rlk_mb_ap_dying,tag=!rlk_mb_inv,distance=..10] run function rlk:boss/apep/org/basic/shd_on
scoreboard players set @s apS 2
scoreboard players set @s apTok 240
