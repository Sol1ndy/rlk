# 런 시작 (@s = player 태그 플레이어). 사용: /function rlk:run/start
# 캐릭터를 초기화(레벨 1, 아이템·골드 없음. 사파이어는 유지)하고 챕터 1의 첫 맵으로 이동
execute unless entity @s[tag=player] run return run tellraw @s {"text":"[런] 'player' 태그가 있는 플레이어로 실행하세요.","color":"red"}
execute unless data storage rlk:room {ready:1b} run return run tellraw @s [{"text":"[런] ","color":"red","bold":true},{"text":"던전 구역이 준비되지 않았습니다. 먼저 ","color":"gray","bold":false},{"text":"/function rlk:room/setup","color":"yellow","bold":false,"click_event":{"action":"suggest_command","command":"/function rlk:room/setup"}},{"text":" 을 실행하세요.","color":"gray","bold":false}]
execute store result score #diff tmp run difficulty
execute if score #diff tmp matches 0 run tellraw @s [{"text":"[런] ","color":"red","bold":true},{"text":"난이도가 '평화로움'이면 몬스터가 나오지 않습니다. (/difficulty easy 이상)","color":"gray","bold":false}]
# 돌아올 자리 기억(런을 이미 진행 중이면 유지)
execute unless score #active room matches 1 run function rlk:run/save_pos
function rlk:player/reset_one
scoreboard players set #active room 1
scoreboard players set #chapter room 1
scoreboard players reset #seen1 room
scoreboard players reset #seen2 room
scoreboard players reset #seen3 room
scoreboard players reset #seen4 room
scoreboard players reset #seen5 room
scoreboard players reset #seen6 room
scoreboard players reset #seen7 room
scoreboard players set #rfCount room 0
scoreboard players set #mapIdx room 0
scoreboard players set #mapType room 0
scoreboard players set #stDefer room 1
execute in minecraft:overworld run function rlk:room/gen
# 시작 아이템 고르기(첫 맵의 시작 자리에서 도감 화면으로)
function rlk:codex/start
# 로노바: 불사의 저주는 맵마다 한 번
scoreboard players set @a[tag=player] rnRev 0
