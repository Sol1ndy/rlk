# @s = a new outward crescent (positioned / rotated as the throw): 1.0 b half width, 1.2 b/t, 10 t,
# wall stop, plain Pyro T1, knockback 0, the group of #q3_g.
tag @s remove rlk_kn_new
tag @s add rlk_kn_out
scoreboard players operation #pjGrp mb = #q3_g kn
scoreboard players set #pjEl mb 1
scoreboard players set #pjKB mb 0
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 1
function rlk:mboss/pj/launch {spd:12,life:10,dmg:31,hr:10}
execute as @s run function rlk:boss/arlecchino/fx/prop/crescent
