execute unless data storage rlk:room rpq[0] run return 1
execute store result score #riftW0 room run data get storage rlk:room rpq[0].wx0
execute store result score #riftW1 room run data get storage rlk:room rpq[0].wz0
execute store result score #riftW2 room run data get storage rlk:room rpq[0].wx1
execute store result score #riftW3 room run data get storage rlk:room rpq[0].wz1
execute if score #riftA0 room >= #riftW0 room if score #riftA1 room <= #riftW2 room if score #riftA2 room >= #riftW1 room if score #riftA3 room <= #riftW3 room run return fail
data remove storage rlk:room rpq[0]
return run function rlk:room/rift/spot/pit_loop
