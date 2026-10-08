# @s = 맞는 몹. 같은 몹(msid)이면 지금까지 쌓인 만큼 피해 증가 후 +1, 다른 몹이면 처음부터
execute unless score @s msid = #huntId itv run scoreboard players set #huntN itv 0
scoreboard players operation #huntId itv = @s msid
scoreboard players operation #t1 itv = #huntN itv
scoreboard players operation #t1 itv *= #huntPer tmp
scoreboard players operation #eb eng += #t1 itv
execute if score #huntN itv < #huntMax tmp run scoreboard players add #huntN itv 1
