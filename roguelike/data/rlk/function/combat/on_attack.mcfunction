# 플레이어 좌클릭(공격) (@s = 공격한 플레이어). atkStrike/몹 실드 클릭 또는 발전과제(몹 직타)에서 호출
advancement revoke @s only rlk:attack
# 아이템 선택 공간에서는 클릭 = 조준한 UI 요소 누르기
execute if score @s pkMode matches 1.. at @s run return run function rlk:lvup/click

# 원소폭발 시전 중 · 불사의 저주로 쓰러져 있는 동안에는 아무것도 할 수 없다
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
# 방금 UI 를 누른 클릭의 두 번째 인식은 무시
execute if score @s uiCd matches 1.. run return 0
# 좌클릭으로 상점 구매/리롤 (처리되면 #shopHandled=1)
execute at @s anchored eyes run function rlk:shop/aim_buy
# 좌클릭으로 방 오브젝트 상호작용 (조준 중인 것)
execute if score #shopHandled tmp matches 0 as @e[tag=rlk_obj,tag=rlk_ohover,limit=1] at @s run function rlk:room/obj/click

# 숄더뷰: 조준 중인 드롭 아이템 버튼(회수/판매) 누르기
execute if score #shopHandled tmp matches 0 unless entity @s[tag=rlk_body] as @e[tag=rlk_dbtn,tag=rlk_dhover,limit=1] at @s run function rlk:ditem/ray_click
# UI(상점·오브젝트·드롭 아이템 버튼)를 누른 클릭이 다음 틱에 한 번 더 들어와 공격·스킬로 이어지지 않게 잠깐 막음
execute if score #shopHandled tmp matches 1 run scoreboard players set @s uiCd 4
execute if score #shopHandled tmp matches 1 run return 0
# 숄더뷰: 공격·스킬은 조준선 쪽으로 몸을 돌린 뒤에(아래의 "at 몸" 이 돌린 방향을 쓰도록)
execute unless entity @s[tag=rlk_body] if entity @e[tag=rlk_av,limit=1] run function rlk:view/face_lock
# 스킬/폭발 아이템을 든 채 좌클릭해도 발동
execute if score #shopHandled tmp matches 0 if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"skill"}}] at @e[tag=rlk_body,limit=1] run return run function rlk:char/cast_skill_l
execute if score #shopHandled tmp matches 0 if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"burst"}}] at @e[tag=rlk_body,limit=1] run return run function rlk:char/cast_burst

# 공격 가능: 개발자 모드이거나, 기본공격 아이템(핫바 0번)을 들고 있을 때만
scoreboard players set #canAtk tmp 0
execute if score @s devMode matches 1 run scoreboard players set #canAtk tmp 1
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run scoreboard players set #canAtk tmp 1

# 구매/리롤이 처리된 클릭은 일반 공격으로 이어지지 않음
# 활: 조준 중이면 발사
execute if score #canAtk tmp matches 1 unless score #shopHandled tmp matches 1 if score #wType tmp matches 2 if score @s bowT matches 1.. at @e[tag=rlk_body,limit=1] run return run function rlk:char/bow/release
execute if score #canAtk tmp matches 1 unless score #shopHandled tmp matches 1 unless score @s atkCD matches 1.. unless score #wType tmp matches 2.. unless score #clShoot tmp matches 1 at @e[tag=rlk_body,limit=1] run function rlk:combat/find
# 법구(로노바): 구체 발사
execute if score #canAtk tmp matches 1 unless score #shopHandled tmp matches 1 unless score @s atkCD matches 1.. if score #wType tmp matches 3 at @e[tag=rlk_body,limit=1] run function rlk:char/ronova/na
execute if score #canAtk tmp matches 1 unless score #shopHandled tmp matches 1 if score #clShoot tmp matches 1 at @e[tag=rlk_body,limit=1] run function rlk:char/clorinde/auto_toggle
execute if score #canAtk tmp matches 1 unless score #shopHandled tmp matches 1 unless score @s atkCD matches 1.. if score #wType tmp matches 2 at @e[tag=rlk_body,limit=1] run function rlk:char/bow/na
