scoreboard players operation #rdSgK rd = @s rdSgStun
scoreboard players set @s rdSgStun 0
function rlk:boss/raiden/finish
# 몽상의 일심 always follows 찰나의 포영, found or not.
execute if score #rdSgK rd matches 1 run scoreboard players set @s rdNext 7
