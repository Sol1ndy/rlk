# 원소폭발 피해(#dmg) × (100 + 전의 × #oathBurst)%. 폭발을 쓴 뒤 이어지는 타격은 소모한 전의(#oathUse)를 쓴다
scoreboard players operation #t1 itv = #oath itv
execute if score #oathT itv matches 1.. run scoreboard players operation #t1 itv = #oathUse itv
scoreboard players operation #t1 itv *= #oathBurst tmp
scoreboard players add #t1 itv 100
scoreboard players operation #dmg tmp *= #t1 itv
scoreboard players operation #dmg tmp /= #100 tmp
