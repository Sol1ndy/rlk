# @s = 격변 반응 피해를 받는 몹. 2개: 피해 증가 / 4개: 플레이어의 치명타 확률·치명타 피해 적용
scoreboard players operation #t1 eng = #lunarDmg tmp
scoreboard players add #t1 eng 100
scoreboard players operation #dmg tmp *= #t1 eng
scoreboard players operation #dmg tmp /= #100 tmp
execute unless score lunar engN matches 4.. run return 0
execute store result score #t1 eng run random value 1..100
execute if score #t1 eng > @a[tag=player,limit=1] critChance run return 0
scoreboard players set #crit tmp 1
# 이 대상에게만 치명타(combat/apply 끝에서 되돌림)
scoreboard players set #frostC eng 1
scoreboard players operation #dmg tmp *= @a[tag=player,limit=1] critDamage
scoreboard players operation #dmg tmp /= #100 tmp
