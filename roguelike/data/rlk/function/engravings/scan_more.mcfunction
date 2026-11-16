# @s = 플레이어. 질주 2개: 닷지 재사용 대기 -#dashEngSpd% (= 기본 × (100 - 감소) / 100, 반올림): 아무것도 피하지 못한 닷지 #dashCoolT 와
# 공격을 피한 닷지 #dashCoolHitT 둘 다
scoreboard players operation #dashCoolT tmp = #dashCoolBase tmp
scoreboard players operation #dashCoolHitT tmp = #dashCoolHitBase tmp
execute if score dash engN matches 2.. run function rlk:engravings/dash/regen
