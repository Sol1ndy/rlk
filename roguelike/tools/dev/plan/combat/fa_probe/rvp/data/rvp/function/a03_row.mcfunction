data modify storage rvp:log row set value {t:0,sel:0,ex:0,dt:-1,cb:-99}
execute store result storage rvp:log row.t int 1 run scoreboard players get #t rvp
execute store result storage rvp:log row.sel int 1 if entity @e[tag=rvpA]
execute store result storage rvp:log row.ex int 1 if entity 00000001-0000-0002-0000-000300000004
execute store result storage rvp:log row.dt int 1 run data get entity 00000001-0000-0002-0000-000300000004 DeathTime
execute store result storage rvp:log row.cb int 1 run scoreboard players get 00000001-0000-0002-0000-000300000004 cb
data modify storage rvp:log row.glow set from entity 00000001-0000-0002-0000-000300000004 Glowing
data modify storage rvp:log row.pos set from entity 00000001-0000-0002-0000-000300000004 Pos
data modify storage rvp:log rows append from storage rvp:log row
scoreboard players add #t rvp 1
execute if score #t rvp matches 36.. run scoreboard players set #mode rvp 0
