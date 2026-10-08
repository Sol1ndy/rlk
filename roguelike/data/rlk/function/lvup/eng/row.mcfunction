# 각인 하나의 줄 (macro: e = 각인 id). 가진 것도 없고 들어올 것도 없으면 줄을 만들지 않는다
scoreboard players set #ec tmp 0
scoreboard players set #ea tmp 0
scoreboard players set #es tmp 0
$execute store result score #ec tmp run scoreboard players get $(e) engCur
$execute store result score #ea tmp run scoreboard players get $(e) engAdd
$execute store result score #es tmp run scoreboard players get $(e) engSub
execute if score #ec tmp matches ..0 if score #ea tmp matches ..0 run return 0
execute if score #engRow tmp matches 18.. run return 0
# 바뀐 뒤 개수 = 지금 - 빠지는 것 + 들어오는 것 (빠지는 것은 '바꿀 아이템 고르기'에서만)
scoreboard players operation #en tmp = #ec tmp
scoreboard players operation #en tmp += #ea tmp
execute if score @s pkMode matches 3 run scoreboard players operation #en tmp -= #es tmp
execute if score @s pkMode matches 5 run scoreboard players operation #en tmp -= #es tmp
execute if score @s pkMode matches 4 if score @s pkHK matches 7 run scoreboard players operation #en tmp -= #es tmp
$data modify storage rlk:lvpick r set value {e:"$(e)",name:"$(e)",color:"white"}
$data modify storage rlk:lvpick r merge from storage rlk:engravings registry.$(e)
execute store result storage rlk:lvpick r.row int 1 run scoreboard players get #engRow tmp
execute store result storage rlk:lvpick r.c int 1 run scoreboard players get #ec tmp
execute store result storage rlk:lvpick r.n int 1 run scoreboard players get #en tmp
# 숫자 색: 늘어남 = 초록, 줄어듦 = 빨강, 조준한 아이템의 각인 = 노랑, 그 밖 = 흰색
data modify storage rlk:lvpick r.nc set value "white"
execute if score #en tmp > #ec tmp run data modify storage rlk:lvpick r.nc set value "#7CDB7C"
execute if score #en tmp < #ec tmp run data modify storage rlk:lvpick r.nc set value "#E06A5A"
execute if score #engStyle tmp matches 1 if score #es tmp matches 1.. run data modify storage rlk:lvpick r.nc set value "#FFE08A"
execute if score #en tmp = #ec tmp run function rlk:lvup/eng/row_plain with storage rlk:lvpick r
execute unless score #en tmp = #ec tmp run function rlk:lvup/eng/row_diff with storage rlk:lvpick r
scoreboard players add #engRow tmp 1
