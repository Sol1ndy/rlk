execute if score @s rdCam matches 1 run return 0
# @s = 플레이어, at @s. 우클릭: 무기(핫바 0번) = 대쉬(활의 조준은 F 키), 스킬(1번) = 원소전투 스킬, 폭발(2번) = 원소폭발
execute if score @s vMap matches 1 run return run function rlk:view/map_right
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"map"}}] run return run function rlk:view/map_right
# 아이템 선택 공간에서는 우클릭 동작 없음
execute if score @s pkMode matches 1.. run return 0
# 원소폭발 시전 중에는 아무것도 할 수 없다
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
# 숄더뷰: 스킬·폭발 아이템이면 조준선 쪽으로 몸을 돌린 뒤에
execute unless entity @s[tag=rlk_body] if entity @e[tag=rlk_av,limit=1] unless items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run function rlk:view/face_lock
execute unless score #wType tmp matches 2 if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] at @e[tag=rlk_body,limit=1] run function rlk:player/dash
execute if score #wType tmp matches 2 if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] at @e[tag=rlk_body,limit=1] run function rlk:char/bow/rdash
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"skill"}}] at @e[tag=rlk_body,limit=1] run function rlk:char/cast_skill_r
execute if items entity @s weapon.mainhand *[minecraft:custom_data~{rlk_ui:{role:"burst"}}] at @e[tag=rlk_body,limit=1] run function rlk:char/cast_burst
