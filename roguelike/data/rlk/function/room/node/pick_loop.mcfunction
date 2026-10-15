# 누적 가중치가 #wr 을 넘는 첫 후보
execute unless data storage rlk:room cand[0] run return 0
execute store result score #cw tmp run data get storage rlk:room cand[0].w
execute if score #wr tmp < #cw tmp run return run execute store result score #nk tmp run data get storage rlk:room cand[0].k
scoreboard players operation #wr tmp -= #cw tmp
data remove storage rlk:room cand[0]
function rlk:room/node/pick_loop
