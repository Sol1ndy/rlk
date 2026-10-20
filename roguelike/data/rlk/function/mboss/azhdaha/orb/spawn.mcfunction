# N5 (macro {tag ring a r w hr y0 y1 dmg grp}; as the body, positioned at the orbit centre): one orb = a marker
# (angle azS x 100 deg, radius azT mb, omega azPT x 100 deg/t) + its hz/disc (#hzRearm 10) that follows it.
execute unless entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] run summon minecraft:marker ~ 201 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_orbc"]}
$summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_orb","$(tag)","rlk_mb_az_onew"]}
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] azS $(a)
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] azT $(r)
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] azPT $(w)
$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] mbS $(ring)
$scoreboard players set #hzY0 mb $(y0)
$scoreboard players set #hzY1 mb $(y1)
$scoreboard players set #azX mb $(grp)
execute if score #azX mb matches 1 run scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzRearm mb 10
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzSfx mb 0
scoreboard players set #hzAct mb 2000
$function rlk:mboss/hz/disc {r:$(hr),tell:1,dmg:$(dmg)}
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_orbhz
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run scoreboard players operation @s azF = #hzLast mb
scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_az_onew] azF = #hzLast mb
tag @e[type=minecraft:marker,tag=rlk_mb_az_onew] remove rlk_mb_az_onew
