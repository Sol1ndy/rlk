# @s = 플레이어. 질주 2개: 닷지 재사용 대기 -#dashEngSpd% (= 기본 × (100 - 감소) / 100)
scoreboard players operation #dashCoolT tmp = #dashCoolBase tmp
execute if score dash engN matches 2.. run function rlk:engravings/dash/regen
