# ccur 을 order 에 추가 (#left 번, 최대 9개까지)
execute store result score #ol tmp run data get storage rlk:pinv order
execute if score #ol tmp matches 9.. run return 0
data modify storage rlk:pinv order append from storage rlk:pinv ccur
scoreboard players remove #left tmp 1
execute if score #left tmp matches 1.. run function rlk:player/inv/collect_add
