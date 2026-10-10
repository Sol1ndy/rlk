function rlk:boss/raiden/object/clear
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-8 ~ ~-4 run function rlk:boss/raiden/object/create {kind:4,model:"lightning_stake",hp:1,id:1,y:0}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~8 ~ ~-4 run function rlk:boss/raiden/object/create {kind:4,model:"lightning_stake",hp:1,id:2,y:0}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~0 ~ ~9 run function rlk:boss/raiden/object/create {kind:4,model:"lightning_stake",hp:1,id:3,y:0}
