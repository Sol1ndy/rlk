# 달의 징조 (@s = 아무나): #lnAll = 감전·개화·결정 전환(콜롬비나 아이템), #lnBl = 개화 전환(콜롬비나 아이템 또는 네페르)
scoreboard players set #lnAll tmp 0
execute if score @a[tag=player,limit=1] it_moon_chalice matches 1.. run scoreboard players set #lnAll tmp 1
scoreboard players operation #lnBl tmp = #lnAll tmp
execute if score #charN tmp matches 8 run scoreboard players set #lnBl tmp 1
