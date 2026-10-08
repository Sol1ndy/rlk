# @s = 플레이어. 지금 리롤 비용 → #pkRerollCost tmp (첫 리롤 0, 그 뒤 #pkRerollStep 씩 증가, 상한 #pkRerollMax)
execute unless score @s pkRr matches 0.. run scoreboard players set @s pkRr 0
scoreboard players operation #pkRerollCost tmp = @s pkRr
scoreboard players operation #pkRerollCost tmp *= #pkRerollStep tmp
execute if score #pkRerollCost tmp > #pkRerollMax tmp run scoreboard players operation #pkRerollCost tmp = #pkRerollMax tmp
