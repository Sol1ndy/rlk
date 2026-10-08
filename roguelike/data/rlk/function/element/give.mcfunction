# 테스트: 가장 가까운 몹(8칸)에 해당 원소를 피해 0 으로 부착 (@s = 플레이어). 사용: /function rlk:element/give {id:"water"}
$execute unless data storage rlk:elem byid."$(id)" run return fail
function rlk:combat/clear_atkflags
$execute store result score #elem tmp run data get storage rlk:elem byid."$(id)".n
scoreboard players set #elU tmp 1000
scoreboard players set #dmg tmp 0
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
execute as @e[tag=rlk_mob,distance=..8,sort=nearest,limit=1] at @s run function rlk:combat/apply
