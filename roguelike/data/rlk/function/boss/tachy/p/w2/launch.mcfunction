# @s = the new crescent display (positioned at her chest, rotated toward the player's chest).
scoreboard players operation #pjEl mb = #el tk
scoreboard players set #pjWall mb 1
scoreboard players set #pjShape mb 0
function rlk:mboss/pj/launch {spd:12,life:30,dmg:42,hr:13}
tag @s remove rlk_tk_new
