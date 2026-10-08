# @s = 준비 중인 플레이어. 지도 영역 한가운데로 옮기고 빈 지도를 쥐여 준다 → 우클릭하면 room/map_bind 가 지도 번호를 기억
tp @s 0.0 200 0.0 0 60
scoreboard players set @s devMode 1
item replace entity @s weapon.mainhand with minecraft:map
scoreboard players set #setup room 1
tellraw @s [{"text":"[방] ","color":"gold","bold":true},{"text":"구역 준비 완료. ","color":"green","bold":false},{"text":"움직이지 말고, 손에 든 빈 지도를 ","color":"white","bold":false},{"text":"우클릭","color":"yellow","bold":true},{"text":"하세요. (던전 지도로 등록됩니다)","color":"white","bold":false}]
function rlk:view/sync
