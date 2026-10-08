# 대쉬 충전 (@s = 플레이어, 충전 수 < 최대일 때 매 틱). 한 번에 1개씩 순차 충전
scoreboard players add @s dashRegen 1
execute if score @s dashRegen >= #dashRegenT tmp run function rlk:player/dash_refill
