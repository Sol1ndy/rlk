# @s = the slab: a blade projectile at the locked feet (its own volley group).
scoreboard players set @s mbId 12
tag @s remove rlk_mb_fg_p12s
tag @s add rlk_mb_fg_p12f
data merge entity @s {teleport_duration:1}
scoreboard players set #pjKB mb 3
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 1
scoreboard players operation #pjGrp mb = #mbGrp mb
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_fg_p12tl,limit=1] feet run function rlk:mboss/pj/launch {spd:15,life:24,dmg:110,hr:8}
playsound minecraft:entity.breeze.shoot hostile @a[tag=player] ~ ~ ~ 0.9 0.6 0.3
playsound minecraft:block.tuff.break hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
