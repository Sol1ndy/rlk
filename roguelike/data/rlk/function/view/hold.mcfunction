# 쉬는 동안(사망·아이템 선택 공간): 달리기 시야 효과만 풀어 둠 · F5 위쪽 시점이면 내리고 원래 크기로
# 받침에서 내리는 틱에는 조준점을 바로 다시 보내도록 카운터를 당겨 둔다(ride_off 가 제목을 지움)
execute if entity @e[tag=rlk_vseat,limit=1] run scoreboard players set #xh view -1
execute if entity @e[tag=rlk_vseat,limit=1] run function rlk:view/ride_off
execute if score #spr view matches 1 run attribute @s minecraft:movement_speed modifier remove rlk:view_sprint
scoreboard players set #spr view 0
# 선택 공간(레벨 업 아이템 선택·인벤토리 상세·도감 등, pkMode 1~)에서도 F5 위쪽 시점이면 3인칭이라 바닐라 조준선이 없다: 조준점을 계속 띄움
execute if score @s pkMode matches 1.. unless score @s dead matches 1 if score #vmode view matches 2 run function rlk:view/sel_xhair
