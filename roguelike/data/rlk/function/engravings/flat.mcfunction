# macro: obj = 플레이어 스탯, pm = 천분율 상수 이름. #dmg 에 스탯 × pm / 1000 을 더한다 (@s = 몹)
$scoreboard players operation #t1 eng = @a[tag=player,limit=1] $(obj)
$scoreboard players operation #t1 eng *= $(pm) tmp
scoreboard players operation #t1 eng /= #1000 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 eng *= @a[tag=player,limit=1] critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 eng /= #100 tmp
scoreboard players operation #dmg tmp += #t1 eng
