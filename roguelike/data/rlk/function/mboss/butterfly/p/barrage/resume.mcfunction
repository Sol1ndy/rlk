# The fight runs again after a pause (core resume hook): every landing marker still waiting gets its decal back
# with the tell it has left (its landing clock mbT - #bfPT; the pause cleared the decals; review fix FX-1).
execute as @e[type=minecraft:marker,tag=rlk_mb_bf_p12t] at @s run function rlk:mboss/butterfly/p/barrage/redraw
