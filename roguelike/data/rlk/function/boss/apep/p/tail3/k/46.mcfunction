# tail3 #apq34T 46
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p34g,limit=1] at @s rotated as @s positioned ^2.4 ^0 ^-0.778 rotated ~-110.72 0 run function rlk:boss/apep/fx/p/crescent_trail {r:120,a:66,dir:-1}
execute at @s run function rlk:boss/apep/fx/snd/q4_swing2
execute if score #mbHitEv mb > #apq34H mb at @s run function rlk:boss/apep/fx/snd/p5_hit
execute if score #mbHitEv mb > #apq34H mb run function rlk:boss/apep/fx/hud/flash_hit
scoreboard players operation #apq34H mb = #mbHitEv mb
