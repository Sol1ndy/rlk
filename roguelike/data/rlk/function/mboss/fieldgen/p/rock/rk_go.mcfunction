# [c_rocks] @s = the slab: a blade projectile at the locked feet (rlk_mb_fg_p6tl), 1.5 b/t, life 24, half width 1.2
# (reach 1.5 b with the framework blade rule), its own volley group.
scoreboard players set @s mbId 6
tag @s remove rlk_mb_fg_p6s
tag @s add rlk_mb_fg_p6f
data merge entity @s {teleport_duration:1}
scoreboard players set #pjKB mb 3
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 1
scoreboard players operation #pjGrp mb = #mbGrp mb
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p6tl,limit=1] feet run function rlk:mboss/pj/launch {spd:15,life:24,dmg:120,hr:12}
execute at @s rotated as @s run function rlk:mboss/fieldgen/fx/p/slab_throw
function rlk:mboss/fieldgen/fx/snd/slab_throw
