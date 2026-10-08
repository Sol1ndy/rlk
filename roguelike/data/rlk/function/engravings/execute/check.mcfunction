# 처형 4개 (@s = 몹): 체력이 최대 체력의 #execHp 퍼센트 이하이면 주는 피해 증가
scoreboard players operation #t1 eng = @s mhpC
scoreboard players operation #t1 eng *= #100 tmp
scoreboard players operation #t2 eng = @s mhpM
scoreboard players operation #t2 eng *= #execHp tmp
execute if score #t1 eng <= #t2 eng run scoreboard players operation #eb eng += #execDmg tmp
