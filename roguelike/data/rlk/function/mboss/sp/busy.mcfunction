# An arena job runs (the special's arena being built / restored / its chunks verified, or another arena's job). The player
# is not moved. Returns 0 (room/rift/enter: 40 t before the next try).
tag @e[tag=rlk_spz] remove rlk_spz
tellraw @a[tag=player] [{text:"[균열] ",color:"#7FD8FF",bold:true},{text:"균열이 아직 안정되지 않았습니다. 잠시 뒤 다시 들어가세요.",color:"gray",bold:false}]
return 0
