# macro: ocur. 이 id의 남은 실물 개수(pcnt)로 유지/드롭 결정 → 같은 아이템 중복 보유 지원
$execute unless data storage rlk:pinv pcnt.$(ocur) run function rlk:player/inv/order_count with storage rlk:pinv
scoreboard players set #okc tmp 0
$execute store result score #okc tmp run data get storage rlk:pinv pcnt.$(ocur)
scoreboard players set #okk tmp 0
execute if score #okc tmp matches 1.. run scoreboard players set #okk tmp 1
execute if score #okk tmp matches 1 run data modify storage rlk:pinv neworder append from storage rlk:pinv ocur
execute if score #okk tmp matches 1 run scoreboard players remove #okc tmp 1
$execute if score #okk tmp matches 1 store result storage rlk:pinv pcnt.$(ocur) int 1 run scoreboard players get #okc tmp
# 실물이 없음 → 클릭해서 버린 것: 발밑에 드롭 (크리에이티브에서는 드롭 없이 목록에서만 제거)
execute if score #okk tmp matches 0 unless entity @s[gamemode=creative] run function rlk:player/inv/order_drop with storage rlk:pinv
