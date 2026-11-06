# A barrier cell (at its centre, y 201): phase 2 only; inside the walk disc; no part inside the Heart's wall exclusion
# r 4.6; never in the player's body box + 1 b (the volume test); never within 1 b of an organism; replace air only;
# each placed block recorded (rlk_mb_ap_wallb, the group id).
execute unless score #apPh mb matches 2 run return 0
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..25] run return 0
execute if entity @e[type=minecraft:marker,tag=rlk_mb_ap_heart,distance=..5.31] run return 0
execute positioned ~-1.5 200 ~-1.5 if entity @e[tag=rlk_body,dx=2,dy=3,dz=2] run return 0
execute positioned ~-1.5 200 ~-1.5 if entity @a[tag=player,dx=2,dy=3,dz=2] run return 0
execute if entity @e[type=minecraft:husk,tag=rlk_mb_ap_org,distance=..1.5] run return 0
execute positioned ~ 201 ~ if block ~ ~ ~ minecraft:air run function rlk:boss/apep/wall/put
execute positioned ~ 202 ~ if block ~ ~ ~ minecraft:air run function rlk:boss/apep/wall/put
