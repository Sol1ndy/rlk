# @s = 상점 이름 패널. 에임되면 펼침(설명), 아니면 접힘(이름). 8틱 유지
execute if score @s shopGid = #shopAimGid tmp run scoreboard players set @s shopOpenT 8
execute if score @s shopOpenT matches 1.. unless entity @s[tag=rlk_shop_open] run function rlk:shop/disp_open
execute if score @s shopOpenT matches ..0 if entity @s[tag=rlk_shop_open] run function rlk:shop/disp_close
execute if score @s shopOpenT matches 1.. run scoreboard players remove @s shopOpenT 1
