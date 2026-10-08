# @s = 정보 디스플레이. 그룹이 에임되면 8틱 유지
execute if score @s dgid = #aimedGid tmp run scoreboard players set @s dopenT 8
execute if score @s dopenT matches 1.. unless entity @s[tag=rlk_dopen] run function rlk:ditem/disp_open
execute if score @s dopenT matches ..0 if entity @s[tag=rlk_dopen] run function rlk:ditem/disp_close
execute if score @s dopenT matches 1.. run scoreboard players remove @s dopenT 1
