# @s = a prop entity the module summoned (item/block display, marker ...), positioned at the launch point,
# rotated = flight direction (pitch counts). {spd: tenths per tick, life: ticks, dmg: % of the base hit
# (0 = visual only), hr: hit radius in tenths}. Options: #pjEl, #pjKB, #pjRet (1 = fly back to the body at
# the end), #pjWall (0 = ignore walls). End events go to the module hook pj_end (#pjEv 1 wall, 2 life,
# 3 returned, 4 hit the player); the prop is killed unless the hook sets #pjKeep mb 1.
tag @s add rlk_mb_pj
tag @s add rlk_mb_aux
tag @s add rlk_room
$scoreboard players set @s mbPjV $(spd)
$scoreboard players set @s mbPjL $(life)
$scoreboard players set @s mbPjD $(dmg)
$scoreboard players set @s mbPjR $(hr)
scoreboard players set @s mbPjT 0
scoreboard players set @s mbPjHit 0
scoreboard players operation @s mbPjE = #mbEl mb
execute if score #pjEl mb matches 0.. run scoreboard players operation @s mbPjE = #pjEl mb
scoreboard players operation @s mbPjB = #pjKB mb
scoreboard players operation @s mbPjRet = #pjRet mb
scoreboard players operation @s mbPjW = #pjWall mb
execute if score @s mbPjR matches 41.. run scoreboard players set @s mbPjR 40
execute if score @s mbPjR matches ..0 run scoreboard players set @s mbPjR 1
tp @s ~ ~ ~ ~ ~
function rlk:mboss/opts_reset
