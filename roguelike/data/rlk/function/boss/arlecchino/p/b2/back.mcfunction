# $(life): the returning wheel (@s = the new prop, rotated toward her).
tag @s remove rlk_kn_new
tag @s add rlk_kn_ret

function rlk:mboss/grp_new
scoreboard players set #pjEl mb 1
scoreboard players set #pjKB mb 0
scoreboard players set #pjWall mb 0
scoreboard players operation #pjGrp mb = #mbGrp mb
$function rlk:mboss/pj/launch {spd:15,life:$(life),dmg:45,hr:11}
