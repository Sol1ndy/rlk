# 선택 공간에서 돌아가기 (@s = 플레이어). 고르지 않은 선택지는 그대로 남는다
function rlk:lvup/cleanup
scoreboard players set #cxWas tmp 0
execute if score @s cxMode matches 1 run scoreboard players set #cxWas tmp 1
scoreboard players set @s cxMode 0
function rlk:lvup/tp_back with storage rlk:lvpick ret
# 교체하며 내려놓은 아이템을 몸(1인칭 = 플레이어, 숄더뷰 = 아바타) 발밑에 떨군다
execute if data storage rlk:lvpick dropq[0] at @e[tag=rlk_body,limit=1] run function rlk:lvup/drop_loop
playsound minecraft:block.portal.trigger master @s ~ ~ ~ 0.25 2.0
# 돌아온 직후의 클릭 무시(확인 클릭의 두 번째 인식이 바닥에 놓인 것의 버튼을 누르지 않게)
scoreboard players set @s uiCd 12
# 시작 아이템 고르기가 끝남: 미뤄 둔 첫 맵 제목
execute if score #cxWas tmp matches 1 if score #stDefer room matches 1 run function rlk:room/title_late
