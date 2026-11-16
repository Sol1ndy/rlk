# @s = 플레이어, at @s (combat/rclick_do). F 와 같은 틱에 온 우클릭: 들고 있던 아이템은 왼손에 있다(오른손은 비어 있음).
# 왼손의 아이템으로 combat/rclick_do 의 세 동작을 그대로: 무기 = 닷지, 스킬 = 원소전투 스킬, 폭발 = 원소폭발
execute unless entity @s[tag=rlk_body] if entity @e[tag=rlk_av,limit=1] unless items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] run function rlk:view/face_lock
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] at @e[tag=rlk_body,limit=1] run function rlk:player/dash
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"skill"}}] at @e[tag=rlk_body,limit=1] run function rlk:char/cast_skill_r
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"burst"}}] at @e[tag=rlk_body,limit=1] run function rlk:char/cast_burst
