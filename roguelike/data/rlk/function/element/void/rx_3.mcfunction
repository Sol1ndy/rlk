# 단죄 (공허+번개): 붉은 낙뢰. 피해 = 반응 기준 × (200 + 잠식 × 8)% + 원소 입자 1개
function rlk:element/calc {m:100}
scoreboard players operation #t tmp = @s rnEr
scoreboard players operation #t tmp *= #c8 tmp
scoreboard players add #t tmp 200
scoreboard players operation #rdmg tmp *= #t tmp
scoreboard players operation #rdmg tmp /= #100 tmp
scoreboard players set @s rxQ 19
scoreboard players operation @s rxDmg = #rdmg tmp
scoreboard players set @s rxEl 3
