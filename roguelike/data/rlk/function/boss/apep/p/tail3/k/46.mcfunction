# tail3 #apq34T 46
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p34g,limit=1] at @s rotated as @s positioned ^-0.186 ^0 ^2.517 rotated ~14.09 0 run function rlk:boss/apep/fx/p/crescent_trail {r:120,a:85,dir:-1}
execute at @s run function rlk:boss/apep/fx/snd/q4_swing2
execute if score #mbHitEv mb > #apq34H mb at @s run function rlk:boss/apep/fx/snd/p5_hit
execute if score #mbHitEv mb > #apq34H mb run function rlk:boss/apep/fx/hud/flash_hit
scoreboard players operation #apq34H mb = #mbHitEv mb
