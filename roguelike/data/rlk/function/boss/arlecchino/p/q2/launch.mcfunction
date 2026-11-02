# @s = the new wheel (rotated toward the lock).
tag @s remove rlk_kn_new
scoreboard players operation #pjGrp mb = #q2_g kn
scoreboard players set #pjEl mb 1
scoreboard players set #pjKB mb 0
scoreboard players set #pjWall mb 1
function rlk:mboss/pj/launch {spd:15,life:10,dmg:36,hr:11}
execute as @s run function rlk:boss/arlecchino/fx/prop/wheel
