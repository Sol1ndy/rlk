# @s/at 유지하며 storage rlk:rep fn 을 #repN 번 반복 실행
$execute if score #repN tmp matches 1.. run function rlk:$(fn)
scoreboard players remove #repN tmp 1
execute if score #repN tmp matches 1.. run function rlk:util/rep_call with storage rlk:rep
