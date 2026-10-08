# 빠른 이동 끝: 스킬이 재사용 대기(#skDashCd)에 들어간다. 뱀의 계략은 남는다
scoreboard players set @s skDash 0
attribute @s minecraft:movement_speed modifier remove rlk:skirk_dash
execute unless score @s skM matches 1.. run attribute @s minecraft:knockback_resistance modifier remove rlk:skirk
scoreboard players operation @s skillCd = #skDashCd tmp
function rlk:char/skirk/cd_reduce
scoreboard players reset 빠른이동 stacks
playsound minecraft:entity.breeze.land master @a ~ ~ ~ 0.5 1.4
