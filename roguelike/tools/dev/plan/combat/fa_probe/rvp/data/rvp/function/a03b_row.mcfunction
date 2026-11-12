data modify storage rvp:log row set value {t:0}
execute store result storage rvp:log row.t int 1 run scoreboard players get #t rvp
execute store result storage rvp:log row.ghost int 1 if entity @e[tag=rlk_cb_ghost]
execute store result storage rvp:log row.mann int 1 if entity @e[type=minecraft:mannequin,tag=rlk_cb_fx]
execute store result storage rvp:log row.near int 1 positioned 4.5 120 0.5 if entity @e[type=minecraft:mannequin,distance=..32]
data modify storage rvp:log row.glow set from entity @e[type=minecraft:mannequin,tag=rlk_cb_fx,limit=1] Glowing
data modify storage rvp:log row.pos set from entity @e[type=minecraft:mannequin,tag=rlk_cb_fx,limit=1] Pos
execute store result storage rvp:log row.box int 1 if entity @e[tag=rlk_dgo]
data modify storage rvp:log rows2 append from storage rvp:log row
scoreboard players add #t rvp 1
execute if score #t rvp matches 14.. run scoreboard players set #mode rvp 0
