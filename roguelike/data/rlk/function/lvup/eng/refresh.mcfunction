# 각인 창 다시 계산·표시 (@s = 플레이어)
# engCur = 지금 가진 아이템들의 각인 개수 / engSub = 조준한 인벤 아이템의 각인 / engAdd = 들어올 아이템(고른 선택지, 또는 조준한 선택지)의 각인
scoreboard players reset * engCur
scoreboard players reset * engAdd
scoreboard players reset * engSub
data modify storage rlk:lvpick iq set from storage rlk:pinv order
function rlk:lvup/eng/cur_loop
# 조준한 인벤 아이템
execute store result storage rlk:lvpick a.h int 1 run scoreboard players get @s pkHI
execute if score @s pkHK matches 2 run function rlk:lvup/eng/sub_inv with storage rlk:lvpick a
# 들어올 아이템: 바꾸는 중이면 고른 선택지, 고르는 중이면 조준한 선택지
execute store result storage rlk:lvpick a.i int 1 run scoreboard players get @s pkSel
execute if score @s pkMode matches 2..3 run function rlk:lvup/eng/add_choice with storage rlk:lvpick a
execute if score @s pkMode matches 5 run function rlk:lvup/eng/add_choice with storage rlk:lvpick a
execute if score @s pkMode matches 5 run function rlk:lvup/eng/sub_swap
execute if score @s pkMode matches 1 if score @s pkHK matches 1 run function rlk:lvup/eng/add_hover with storage rlk:lvpick a
# 인벤토리 상세: 판매 버튼을 조준하면 고른 아이템의 각인이 빠진 모습을 보여 준다
execute if score @s pkMode matches 4 if score @s pkHK matches 7 run function rlk:invd/eng_sel
# 표시 방식: 0 그대로 / 1 조준한 아이템의 각인 강조(고르는 중 + 인벤 조준) / 2 변화 표시
scoreboard players set #engStyle tmp 2
execute if score @s pkMode matches 1 if score @s pkHK matches 2 run scoreboard players set #engStyle tmp 1
execute if score @s pkMode matches 4 if score @s pkHK matches 2 run scoreboard players set #engStyle tmp 1
execute as @e[tag=rlk_pk_er] run data modify entity @s text set value {text:""}
scoreboard players set #engRow tmp 0
data modify storage rlk:lvpick gq set from storage rlk:engravings ids
function rlk:lvup/eng/row_loop
execute if score #engRow tmp matches 0 run data modify entity @e[tag=rlk_pk_er,scores={pkIdx=0},limit=1] text set value {text:"(각인 없음)",color:"dark_gray"}
