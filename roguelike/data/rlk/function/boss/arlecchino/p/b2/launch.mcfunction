# @s = the new outward wheel (positioned / rotated as the release).
tag @s remove rlk_kn_new
tag @s add rlk_kn_out
function rlk:boss/arlecchino/fx/prop/wheel
function rlk:mboss/grp_new
scoreboard players set #pjEl mb 1
scoreboard players set #pjKB mb 0
scoreboard players set #pjWall mb 1
scoreboard players operation #pjGrp mb = #mbGrp mb
function rlk:mboss/pj/launch {spd:15,life:11,dmg:36,hr:11}
