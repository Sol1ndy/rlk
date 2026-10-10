function rlk:boss/raiden/object/clear
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-10 ~ ~-6 run function rlk:boss/raiden/object/create {kind:1,model:"electro_orb",hp:3,id:1,y:0.3}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~10 ~ ~-6 run function rlk:boss/raiden/object/create {kind:1,model:"electro_orb",hp:3,id:2,y:0.3}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~ ~ ~11 run function rlk:boss/raiden/object/create {kind:1,model:"electro_orb",hp:3,id:3,y:0.3}
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 0.7 0.3
