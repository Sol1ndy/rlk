# $(life) $(g) $(kb): the returning crescent (@s = the new prop, rotated toward her).
tag @s remove rlk_kn_new
tag @s add rlk_kn_ret
$scoreboard players set #pjGrp mb $(g)
$scoreboard players set #pjKB mb $(kb)
scoreboard players set #pjEl mb 1
scoreboard players set #pjWall mb 0
scoreboard players set #pjShape mb 1
$function rlk:mboss/pj/launch {spd:12,life:$(life),dmg:26,hr:10}
execute as @s run function rlk:boss/arlecchino/fx/prop/crescent
