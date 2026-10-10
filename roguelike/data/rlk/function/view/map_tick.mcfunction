# 지도 화면: 이동/마우스로 지도 바깥을 볼 수 없게 매 틱 고정한다.
execute if score @s dead matches 1 run return run function rlk:view/map_close
execute unless score #active room matches 1 run return run function rlk:view/map_close
execute if score #combat room matches 1.. run return run function rlk:view/map_close
execute unless entity @e[tag=rlk_body,limit=1] run return run function rlk:view/map_close
scoreboard players add @s vMapT 1
function rlk:view/map_position
function rlk:view/map_marker
# 무기를 다른 슬롯으로 바꾸어도 지도 화면의 클릭은 닫기만 수행한다.
execute if score @s rcU matches 1 run function rlk:combat/rc_hold
execute unless score @s rcU matches 1 run scoreboard players set @s rcT 0
scoreboard players set @s rcU 0
