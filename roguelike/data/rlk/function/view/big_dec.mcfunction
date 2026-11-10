# @s = 플레이어 (view/tick: vBig 1..). 큰 제목의 남은 틱을 줄이고, 끝난 틱(0)에는 F5 조준점을 바로 다시 보내게 한다
# (view/ride_tick 의 10틱 셈 #xh view 를 9 로: 같은 틱의 뒤쪽에서 0 이 되어 view/xhair). 패링 · 닷지 덮개가 끝날 때마다 조준점이
# 최대 9틱 늦게 돌아오던 것을 없앤다
scoreboard players remove @s vBig 1
execute if score @s vBig matches 0 run scoreboard players set #xh view 9
