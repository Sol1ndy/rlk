# @s = a 파괴: 1 rolling to the nearest stop (r 2.6 off the socket bearings) at 0.1 b/t, 2 the fuse (contact + 61: the blast).
execute if score @s apS matches 2 run return run function rlk:boss/apep/org/destr/fuse
execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_dstop,distance=..0.2] run return run function rlk:boss/apep/org/destr/contact
execute facing entity @e[type=minecraft:marker,tag=rlk_mb_ap_dstop,sort=nearest,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.1}
function rlk:boss/apep/om/face
scoreboard players operation #apM mb = @s apT
scoreboard players operation #apM mb %= #apK8 mb
execute if score #apM mb matches 0 at @s run function rlk:boss/apep/fx/snd/o7_roll
