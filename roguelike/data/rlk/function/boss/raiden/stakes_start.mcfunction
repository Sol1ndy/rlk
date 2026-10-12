function rlk:boss/raiden/object/clear
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~0 ~ ~-1.6 run function rlk:boss/raiden/object/create {kind:4,model:"lightning_stake",hp:1,id:1,y:0}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~1.4 ~ ~0.8 run function rlk:boss/raiden/object/create {kind:4,model:"lightning_stake",hp:1,id:2,y:0}
execute at @e[tag=rlk_raiden_arena,limit=1] run execute positioned ~-1.4 ~ ~0.8 run function rlk:boss/raiden/object/create {kind:4,model:"lightning_stake",hp:1,id:3,y:0}
