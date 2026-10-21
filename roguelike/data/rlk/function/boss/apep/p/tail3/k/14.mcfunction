# tail3 #apq34T 14
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p34f,limit=1] at @s rotated as @s positioned ^2.317 ^0 ^1.781 rotated ~-22.2 0 run function rlk:boss/apep/fx/p/crescent_trail {r:120,a:61,dir:1}
execute at @s run function rlk:boss/apep/fx/snd/q4_swing
execute if score #mbHitEv mb > #apq34H mb at @s run function rlk:boss/apep/fx/snd/p5_hit
execute if score #mbHitEv mb > #apq34H mb run function rlk:boss/apep/fx/hud/flash_hit
scoreboard players operation #apq34H mb = #mbHitEv mb
