# Resume: the following ring (before lock 1) or the held target disc again (the pause cleared them).
execute if score #apq33T mb matches 10..32 at @e[type=minecraft:marker,tag=rlk_mb_ap_p33r,limit=1] run function rlk:boss/apep/fx/tele/mring {id:0,r:36,el:22}
execute as @e[type=minecraft:marker,tag=rlk_mb_ap_p33k] at @s run function rlk:boss/apep/p/shells/redraw
