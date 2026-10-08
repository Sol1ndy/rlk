# 첫 구역 (@s = 구역 표식, at @s): 방문 완료 처리. 나무뿌리 맵 = 뿌리 생성, 레벨업 맵 = 경험치 지점 예약
scoreboard players set @s zst 3
function rlk:room/cells_kill
function rlk:room/zone_mark
execute if score @s zkind matches 8 run function rlk:room/spot with storage rlk:room cur.spot
execute if score @s zkind matches 10 run function rlk:room/spot with storage rlk:room cur.spot
