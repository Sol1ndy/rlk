# At the star spot (floor): aux husk with its own pool (per mille of the body max HP), RES and kind, plus the
# glyph visual. #gdSk = kind (1-4 element, 5/6 inert), #gdSs = slot.
scoreboard players set #gdPm mb 70
scoreboard players set #auxRes mb 0
execute if score #gdSk mb matches 5.. run scoreboard players set #gdPm mb 17
execute if score #gdSk mb matches 5.. run scoreboard players set #auxRes mb 80
function rlk:mboss/guardian/star/pool
function rlk:mboss/aux/spawn
tag @e[tag=rlk_mb_auxlast,limit=1] add rlk_mb_gd_star
scoreboard players operation @e[tag=rlk_mb_auxlast,limit=1] mbS = #gdSk mb
scoreboard players operation @e[tag=rlk_mb_auxlast,limit=1] mbId = #gdSs mb
scoreboard players set @e[tag=rlk_mb_auxlast,limit=1] mbT 0
execute if score #gdSk mb matches 1 run function rlk:mboss/guardian/star/vis1
execute if score #gdSk mb matches 2 run function rlk:mboss/guardian/star/vis2
execute if score #gdSk mb matches 3 run function rlk:mboss/guardian/star/vis3
execute if score #gdSk mb matches 4 run function rlk:mboss/guardian/star/vis4
execute if score #gdSk mb matches 5 run function rlk:mboss/guardian/star/vis5
execute if score #gdSk mb matches 6 run function rlk:mboss/guardian/star/vis6
scoreboard players operation @e[type=minecraft:text_display,tag=rlk_mb_gd_svnew,limit=1] mbId = #gdSs mb
scoreboard players set @e[type=minecraft:text_display,tag=rlk_mb_gd_svnew,limit=1] mbT 0
tag @e[type=minecraft:text_display,tag=rlk_mb_gd_svnew] remove rlk_mb_gd_svnew
particle minecraft:block{block_state:"minecraft:red_concrete"} ~ ~0.6 ~ 0.3 0.3 0.3 0 8 force @a[tag=player]
scoreboard players add #gdStars mb 1
