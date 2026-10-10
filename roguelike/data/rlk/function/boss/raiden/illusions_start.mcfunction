function rlk:boss/raiden/object/clear
execute store result score #rdReal rd run random value 1..4
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-8 ~ ~-8 run function rlk:boss/raiden/object/create {kind:2,model:"illusion",hp:1,id:1,y:1}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~8 ~ ~-8 run function rlk:boss/raiden/object/create {kind:2,model:"illusion",hp:1,id:2,y:1}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-8 ~ ~8 run function rlk:boss/raiden/object/create {kind:2,model:"illusion",hp:1,id:3,y:1}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~8 ~ ~8 run function rlk:boss/raiden/object/create {kind:2,model:"illusion",hp:1,id:4,y:1}
execute as @e[tag=rlk_rd_object,scores={rdObjKind=2}] if score @s rdObjId = #rdReal rd run scoreboard players set @s rdReal 1
