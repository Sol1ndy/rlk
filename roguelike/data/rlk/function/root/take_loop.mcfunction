# rq 에서 무작위로 하나씩 rootc 로 (rootc 가 3개가 되거나 rq 가 빌 때까지)
execute store result score #rn tmp run data get storage rlk:room rootc
execute if score #rn tmp matches 3.. run return 0
execute store result score #rl tmp run data get storage rlk:room rq
execute if score #rl tmp matches ..0 run return 0
execute store result score #r tmp run random value 0..999
scoreboard players operation #r tmp %= #rl tmp
execute store result storage rlk:room a.r int 1 run scoreboard players get #r tmp
function rlk:root/take_one with storage rlk:room a
function rlk:root/take_loop
