execute if score @s dead matches 1 run scoreboard players set @s arSk 0
execute unless score @s arSk matches 1.. run return 0
execute if score @s pmActive matches 1 if data storage rlk:player_motion active{char:"arle",clip:"skill"} run return 0
# 사라져 있는 중 (@s = 플레이어, at 몸)
scoreboard players remove @s arSk 1
execute if score @s arSk matches ..0 run function rlk:char/arlecchino/skill_go
