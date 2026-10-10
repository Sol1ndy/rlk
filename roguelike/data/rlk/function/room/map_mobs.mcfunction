# 지도 위 적 표시 (@s = 플레이어, 왼손에 던전 지도). 10틱마다
data modify storage rlk:room mdm.dec set value {}
data modify storage rlk:room mdm.map_id set from storage rlk:room map_id
scoreboard players set #mdi tmp 0
execute as @e[tag=rlk_mob,limit=48] run function rlk:room/map_mob
# 바뀐 게 없으면 다시 쓰지 않는다(손이 출렁이지 않게)
data modify storage rlk:room mdChk set from storage rlk:room mdm.dec
execute store success score #mdc tmp run data modify storage rlk:room mdChk set from storage rlk:room mdPrev
execute unless data storage rlk:room mdPrev run scoreboard players set #mdc tmp 1
execute if score #mdc tmp matches 0 run return 0
data modify storage rlk:room mdPrev set from storage rlk:room mdm.dec
function rlk:room/map_set with storage rlk:room mdm
