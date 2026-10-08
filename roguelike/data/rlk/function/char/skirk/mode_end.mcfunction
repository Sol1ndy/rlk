# 일곱빛 섬광 끝: 남은 뱀의 계략과 고갈이 사라지고, 스킬이 재사용 대기에 들어간다
scoreboard players set @s skM 0
scoreboard players set #skMode tmp 0
scoreboard players set @s energy 0
scoreboard players set @s skDep 0
scoreboard players set @s skDepCd 0
scoreboard players operation @s skillCd = #skillCdT tmp
function rlk:char/skirk/cd_reduce
scoreboard players set @s buShown -1
attribute @s minecraft:knockback_resistance modifier remove rlk:skirk
scoreboard players reset 일곱빛섬광 stacks
scoreboard players reset 고갈 stacks
playsound minecraft:block.beacon.deactivate master @a ~ ~ ~ 0.7 1.8
particle minecraft:snowflake ~ ~1 ~ 0.5 0.7 0.5 0.05 20
