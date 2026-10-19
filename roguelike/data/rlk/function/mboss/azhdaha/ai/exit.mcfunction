# The P7 exit test (plan 5 P7; generated from api WHIP_*): one of the three exits lies within 7.2 b of the
# player: (1) the unswept half behind the rump (f <= -4.8, the other side), (2) the HEAD lane within
# 65 degrees of the front axis, (3) beyond the tip (> 17.05 b from the anchor). Tenths.
scoreboard players set #azExit mb 0
# (1) |s| when behind the rump, else hypot(|s|, f - tail_f)
scoreboard players operation #azX mb = #azSt mb
execute if score #azX mb matches ..-1 run scoreboard players operation #azX mb *= #cm1 mb
scoreboard players operation #azY mb = #azFt mb
scoreboard players remove #azY mb -48
execute if score #azY mb matches ..0 run scoreboard players set #azY mb 0
scoreboard players operation #azZ mb = #azX mb
scoreboard players operation #azZ mb *= #azX mb
scoreboard players operation #azY mb *= #azY mb
scoreboard players operation #azZ mb += #azY mb
execute if score #azZ mb matches ..5184 run scoreboard players set #azExit mb 1
# (2) the head lane: inside the cone, or within R of its boundary ray (|s| cos65 - f sin65 <= R)
scoreboard players set #azY mb 4226
scoreboard players operation #azY mb *= #azX mb
scoreboard players set #azZ mb 9063
scoreboard players operation #azZ mb *= #azFt mb
scoreboard players operation #azY mb -= #azZ mb
execute if score #azY mb matches ..720000 if score #azFt mb matches 0.. run scoreboard players set #azExit mb 1
# (3) beyond the tip: the anchor distance >= tip - R
scoreboard players operation #azZ mb = #azDist mb
scoreboard players operation #azZ mb *= #azDist mb
execute if score #azZ mb matches 9702.. run scoreboard players set #azExit mb 1
