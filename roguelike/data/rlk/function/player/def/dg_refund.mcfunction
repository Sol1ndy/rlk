# @s = 플레이어. 이번 닷지가 공격을 피했다(퍼펙트 · 넓은 닷지; 닷지 한 번에 한 번, #dgRf cb = 그 닷지의 dgAt): 재사용 대기를
# #dashCoolT - #dashCoolHitT 틱 돌려준다(아무것도 피하지 못한 닷지 18틱 → 피한 닷지 12틱; 질주 2개 14 → 10)
scoreboard players operation #dgRf cb = @s dgAt
scoreboard players operation #t cb = #dashCoolT tmp
scoreboard players operation #t cb -= #dashCoolHitT tmp
scoreboard players operation @s dashCool -= #t cb
execute if score @s dashCool matches ..-1 run scoreboard players set @s dashCool 0
