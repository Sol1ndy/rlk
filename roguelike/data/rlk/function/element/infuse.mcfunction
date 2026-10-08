# 기본공격 원소 부여 (@s = 플레이어). 사용: /function rlk:element/infuse {id:"wind"}
# id: physical(해제) fire water thunder ice rock wind grass  (한글 불/물/번개/얼음/바위/바람/풀/물리, pyro/hydro/electro/cryo/geo/anemo/dendro 도 가능)
# 다시 부르거나 physical 을 줄 때까지 유지. 시간 제한은 element/infuse_for {id:"fire",sec:10}
$execute unless data storage rlk:elem byid."$(id)" run return run tellraw @s [{"text":"[원소 부여] ","color":"red"},{"text":"알 수 없는 원소: $(id)  (physical, fire, water, thunder, ice, rock, wind, grass)","color":"gray"}]
$execute store result score @s infuse run data get storage rlk:elem byid."$(id)".n
scoreboard players set @s infuseT -1
$data modify storage rlk:hud inf set from storage rlk:elem byid."$(id)".tag
execute if score @s infuse matches 1.. run tellraw @s [{"text":"[원소 부여] ","color":"gold"},{"nbt":"inf","storage":"rlk:hud","interpret":true},{"text":"기본공격에 부여됨","color":"gray"}]
execute if score @s infuse matches 0 run tellraw @s [{"text":"[원소 부여] ","color":"gold"},{"text":"해제 (물리)","color":"gray"}]
