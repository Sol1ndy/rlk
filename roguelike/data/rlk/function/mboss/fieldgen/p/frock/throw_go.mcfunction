# @s = the slab: a blade projectile at the locked feet (1.5 b/t, life 24, hr 0.8 = reach 1.45 b, its own group).
scoreboard players set @s mbId 12
tag @s remove rlk_mb_fg_p12s
tag @s remove rlk_mb_fg_p12r
tag @s add rlk_mb_fg_p12f
data merge entity @s {teleport_duration:1}
scoreboard players set #pjKB mb 3
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 1
scoreboard players operation #pjGrp mb = #mbGrp mb
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p12tl,limit=1] feet run function rlk:mboss/pj/launch {spd:15,life:24,dmg:110,hr:8}
execute at @s rotated as @s run function rlk:mboss/fieldgen/fx/p/slab_throw
function rlk:mboss/fieldgen/fx/snd/slab_throw
