# @s = 플레이어 (player/hotbar/tick 에서: F 로 무기·스킬·폭발 아이템이 왼손에 넘어옴, 웅크리지 않음). 아이템 회수는 부른 쪽이 한다
execute if score @s pkMode matches 1.. run return 0
execute if score @s dead matches 1 run return 0
execute if score @s buT matches 1.. run return 0
execute if score @s rnDie matches 1.. run return 0
# 활: 무기를 든 채 F = 조준 시작/취소 (대쉬는 우클릭)
execute if score #wType tmp matches 2 unless entity @s[tag=rlk_body] if entity @e[tag=rlk_av,limit=1] if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run function rlk:view/face_lock
execute if score #wType tmp matches 2 if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] at @e[tag=rlk_body,limit=1] run return run function rlk:char/bow/toggle
execute at @e[tag=rlk_body,limit=1] run function rlk:player/dash
