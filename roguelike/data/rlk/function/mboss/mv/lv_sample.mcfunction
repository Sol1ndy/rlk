# From mboss/world (chapter fights, live and unpaused): the lockv ring buffer rlk:mboss lv[0..5] (oldest .. newest) of
# the player's body x / z in milliblocks; a tick while the player dashes (dashMoveT >= 1) is skipped (cm.md 13.1).
execute if entity @a[tag=player,scores={dashMoveT=1..},limit=1] run return 0
execute unless function rlk:mboss/mv/plpos run return 0
scoreboard players operation #lx mb = #mbPX mb
scoreboard players operation #lz mb = #mbPZ mb
execute unless data storage rlk:mboss lv[5] run function rlk:mboss/mv/lv_fill
data modify storage rlk:mboss lv append value {x:0,z:0}
data remove storage rlk:mboss lv[0]
execute store result storage rlk:mboss lv[5].x int 1 run scoreboard players get #lx mb
execute store result storage rlk:mboss lv[5].z int 1 run scoreboard players get #lz mb
scoreboard players add #mbQi mb 1
execute if score #mbQi mb matches 6.. run scoreboard players set #mbQi mb 0
