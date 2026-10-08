# @s = 준비 중인 플레이어, 방금 만든 지도를 손에 들고 있음 → 지도 번호 저장
execute store result storage rlk:room map_id int 1 run data get entity @s SelectedItem.components."minecraft:map_id"
item replace entity @s weapon.mainhand with minecraft:air
scoreboard players set #setup room 0
tag @s remove rlk_setup
data modify storage rlk:room ready set value 1b
data modify storage rlk:room area set value "s0"
function rlk:dev/off
tellraw @s [{"text":"[방] ","color":"gold","bold":true},{"text":"던전 지도 등록 완료. ","color":"green","bold":false},{"text":"/function rlk:run/start","color":"yellow","bold":false,"click_event":{"action":"suggest_command","command":"/function rlk:run/start"}},{"text":" 로 시작합니다.","color":"white","bold":false}]
