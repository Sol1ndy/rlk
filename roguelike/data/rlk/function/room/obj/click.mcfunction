# @s = 조준 중인 오브젝트, at @s. 좌클릭 처리 (일반 공격으로 이어지지 않게 #shopHandled)
scoreboard players set #shopHandled tmp 1
execute if score #combat room matches 1.. run return 0
execute if score @s oact matches 1 run return run function rlk:room/obj/do_money
execute if score @s oact matches 2 run return run function rlk:room/obj/do_sapphire
execute if score @s oact matches 3 run return run tellraw @a[tag=player] [{"text":"상인: ","color":"#6FCF8F"},{"text":"진열대의 가격표를 눌러 고르게. 회복도 판다네.","color":"gray"}]
execute if score @s oact matches 4 run return run tellraw @a[tag=player] [{"text":"[재련] ","color":"#C9C9C9"},{"text":"아직 사용할 수 없습니다. (준비 중)","color":"gray"}]
execute if score @s oact matches 5 run return run function rlk:ench/obj
execute if score @s oact matches 6 run scoreboard players operation #rootG room = @s ogid
execute if score @s oact matches 6 run return run execute as @a[tag=player,limit=1] at @s run function rlk:root/open
# 보스전 선택지(oact 7, oarg 8). 예전 판의 맵 종류 선택지(oarg 1~7)는 노드 맵으로 바꿔 진행
execute if score @s oact matches 7 if score @s oarg matches 1..7 run return run function rlk:room/node/legacy
execute if score @s oact matches 7 run scoreboard players operation #mapType room = @s oarg
execute if score @s oact matches 7 run return run function rlk:run/next_map
# 노드 선택지(oarg = 선택지 번호)
execute if score @s oact matches 9 run return run function rlk:room/node/choose
# 노드 구역 오브젝트: 10 주사위, 11 보유 칸, 12 생명력, 13 아이템
execute if score @s oact matches 10 run return run function rlk:room/obj/do_dice
execute if score @s oact matches 11 run return run function rlk:room/obj/do_slot
execute if score @s oact matches 12 run return run function rlk:room/obj/do_hp
execute if score @s oact matches 13 run return run function rlk:room/obj/do_item
# 중간보스 문(oact 14): 구역 전투 시작 → 경기장
execute if score @s oact matches 14 run return run function rlk:mboss/gate
# 중간보스 아이템 상자(oact 15, 처치 뒤 문 자리에 떨어짐): 상자 하나 = 챕터 등급 아이템 선택 1번(열린 상자는 선택 화면만 다시 엶)
execute if score @s oact matches 15 run return run function rlk:room/obj/do_mbox
# 챕터 보스 문(oact 16, 입구 구역 한가운데): 경기장 준비가 끝났으면 구역 전투 시작 → 경기장
execute if score @s oact matches 16 run return run function rlk:mboss/cb/gate
# rift (build_rift.py)
execute if score @s oact matches 17 run return run function rlk:room/rift/click
execute if score @s oact matches 8 run return run function rlk:run/next_chapter
