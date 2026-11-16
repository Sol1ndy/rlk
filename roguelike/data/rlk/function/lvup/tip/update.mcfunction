# 조준한 요소의 설명 (@s = 플레이어)
data modify storage rlk:lvpick tip set value []
execute store result storage rlk:lvpick a.h int 1 run scoreboard players get @s pkHI
execute if score @s pkHK matches 1 run function rlk:lvup/tip/choice with storage rlk:lvpick a
execute if score @s pkHK matches 2 run function rlk:lvup/tip/inv with storage rlk:lvpick a
execute if score @s pkHK matches 9 run function rlk:lvup/tip/char
execute if score @s pkHK matches 13 run function rlk:codex/tip
execute if score @s pkHK matches 14 if score @s pkMode matches 7 run function rlk:root/tip with storage rlk:lvpick a
execute if score @s pkHK matches 2 if score @s pkMode matches 8 run function rlk:ench/tip with storage rlk:lvpick a
execute if score @s pkHK matches 3 run data modify storage rlk:lvpick tip set value [{text:"리롤\n",color:"#FFE08A"},{text:"선택지를 새로 뽑습니다.\n",color:"white"},{text:"첫 번째는 무료, 그 뒤로는 주사위가\n하나씩 듭니다. 주사위가 없으면 못 합니다.",color:"gray"}]
execute if score @s pkHK matches 4 run data modify storage rlk:lvpick tip set value [{text:"넘기기\n",color:"#C9C9C9"},{text:"이번 선택을 포기합니다.\n포기한 기회는 돌아오지 않습니다.",color:"white"}]
execute if score @s pkHK matches 7 run data modify storage rlk:lvpick tip set value [{text:"판매\n",color:"#FFE08A"},{text:"고른 아이템을 팔고 골드를 얻습니다.\n가격은 아이템 등급에 따라 정해집니다.",color:"white"}]
# 빈 목록은 글자로 만들 수 없다({text:"",extra:[]} 오류) → 비어 있으면 빈 글자
execute if data storage rlk:lvpick tip[0] run function rlk:lvup/tip/set with storage rlk:lvpick
execute unless data storage rlk:lvpick tip[0] run data modify entity @e[tag=rlk_pk_tip,limit=1] text set value {text:""}
# 인벤토리 상세: 각인 설명 창
execute if score @s pkMode matches 4 run function rlk:invd/tip2
execute if score @s pkMode matches 6 run function rlk:codex/tip2
