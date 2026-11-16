# 받은 F(패링 입력, player/def/press) 때 아이템 효과 (@s = 플레이어, at @s). 지금은 튜토리얼 1단계의 횟수만
execute if score #tutS lob matches 1 if score @s lobRoom matches 2 run scoreboard players add #tutC lob 1
