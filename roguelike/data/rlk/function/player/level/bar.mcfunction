# 경험치 바 = 레벨/경험치 표시 (@s = 플레이어, 매 틱). 바닐라 경험치가 다르면 맞춰 놓음
# 바닐라 기준 이 레벨의 바 길이(#lvVn): ~15 → 2L+7, 16~30 → 5L−38, 31~ → 9L−158
scoreboard players operation #lvVn tmp = @s level
execute if score @s level matches ..15 run scoreboard players operation #lvVn tmp *= #st2 tmp
execute if score @s level matches ..15 run scoreboard players add #lvVn tmp 7
execute if score @s level matches 16..30 run scoreboard players operation #lvVn tmp *= #c5 tmp
execute if score @s level matches 16..30 run scoreboard players remove #lvVn tmp 38
execute if score @s level matches 31.. run scoreboard players operation #lvVn tmp *= #c9 tmp
execute if score @s level matches 31.. run scoreboard players remove #lvVn tmp 158
scoreboard players operation #lvPt tmp = @s xp
scoreboard players operation #lvPt tmp *= #lvVn tmp
scoreboard players operation #lvPt tmp /= @s xpNeed
execute if score #lvPt tmp >= #lvVn tmp run scoreboard players operation #lvPt tmp = #lvVn tmp
execute if score #lvPt tmp >= #lvVn tmp run scoreboard players remove #lvPt tmp 1
execute if score #lvPt tmp matches ..-1 run scoreboard players set #lvPt tmp 0
execute store result score #lvQl tmp run experience query @s levels
execute store result score #lvQp tmp run experience query @s points
execute if score #lvQl tmp = @s level if score #lvQp tmp = #lvPt tmp run return 0
execute store result storage rlk:pl l int 1 run scoreboard players get @s level
execute store result storage rlk:pl p int 1 run scoreboard players get #lvPt tmp
function rlk:player/level/bar_set with storage rlk:pl
