# macro: ccur. order 에 반영되지 않은 실물 개수(#left)만큼 order 에 추가
$execute unless data storage rlk:pinv pcnt.$(ccur) run function rlk:player/inv/order_count {ocur:"$(ccur)"}
scoreboard players set #left tmp 0
$execute store result score #left tmp run data get storage rlk:pinv pcnt.$(ccur)
execute if score #left tmp matches 1.. run function rlk:player/inv/collect_add
