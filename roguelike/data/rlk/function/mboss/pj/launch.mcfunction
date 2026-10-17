# @s = a prop entity the module summoned (item/block display, marker ...), positioned at the launch point,
# rotated = flight direction (pitch counts). {spd: tenths per tick, life: ticks, dmg: % of the base hit
# (0 = visual only), hr: hit radius in tenths}. Options: #pjEl, #pjKB, #pjRet (1 = fly back to the body's
# eyes at the end), #pjWall (0 = ignore walls). Events go to the module hook pj_end with #pjEv 1 wall,
# 2 life over, 3 back at the body (or the return time ran out), 4 hit the player; #pjKeep mb is preset to
# the default and the hook may flip it: 1 = the prop lives on (4: keeps flying, it pierces; 1/2 of a
# returning prop: flies back; otherwise released as a plain entity), 0 = removed at once.
# Refused while the boss is dying (#mbSt 2): the prop is removed.
execute if score #mbSt mb matches 2 run function rlk:mboss/opts_reset
execute if score #mbSt mb matches 2 run return run kill @s
scoreboard players set #mbPjOn mb 1
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
