# 고통&절망: 액션 시 2초 공속/이속 버프 스택 (최대 20)
scoreboard players add @s pdStack 1
execute if score @s pdStack matches 21.. run scoreboard players set @s pdStack 20
scoreboard players set @s pdT 40
