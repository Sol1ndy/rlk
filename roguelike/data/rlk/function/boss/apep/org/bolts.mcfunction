# Any executor, every phase-2 tick: a bolt within 1.5 b of the Heart's bulb box (a 6.2 b square, y 199.95..205.25) hits the Heart
# and ends; the comet trail every 2 t (#apClk2 = 0).
execute as @e[type=minecraft:item_display,tag=rlk_mb_ap_bolt] positioned 436.9 199.95 4.9 if entity @s[dx=5.2,dy=4.3,dz=5.2] at @s run function rlk:boss/apep/org/bolt_hit
execute if score #apClk2 mb matches 0 as @e[type=minecraft:item_display,tag=rlk_mb_ap_bolt] at @s run function rlk:boss/apep/fx/p/comet_trail
