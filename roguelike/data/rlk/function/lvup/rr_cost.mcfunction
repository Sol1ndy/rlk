# @s = 플레이어. 지금 리롤 비용(주사위 수) → #pkRerollCost tmp. 이번 선택의 첫 리롤은 무료, 그 뒤로는 매번 주사위 #pkRerollDice 개(오르지 않음)
execute unless score @s pkRr matches 0.. run scoreboard players set @s pkRr 0
scoreboard players set #pkRerollCost tmp 0
execute if score @s pkRr matches 1.. run scoreboard players operation #pkRerollCost tmp = #pkRerollDice tmp
