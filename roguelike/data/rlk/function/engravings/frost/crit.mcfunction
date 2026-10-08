# @s = 빙결된 몹. 치명타가 아니었던 타격을 확률로 치명타로: 전체 치명타 확률이 정확히 +#frostCrit 포인트가 되도록, 남은 확률 중에서 뽑는다
#   성공 기준 = #frostCrit × 100 / (100 - 치명타 확률)
scoreboard players set #t1 eng 100
scoreboard players operation #t1 eng -= @a[tag=player,limit=1] critChance
execute if score #t1 eng matches ..0 run return 0
scoreboard players operation #t2 eng = #frostCrit tmp
scoreboard players operation #t2 eng *= #100 tmp
scoreboard players operation #t2 eng /= #t1 eng
execute store result score #t1 eng run random value 1..100
execute if score #t1 eng > #t2 eng run return 0
scoreboard players set #crit tmp 1
scoreboard players set #frostC eng 1
scoreboard players operation #dmg tmp *= @a[tag=player,limit=1] critDamage
scoreboard players operation #dmg tmp /= #100 tmp
