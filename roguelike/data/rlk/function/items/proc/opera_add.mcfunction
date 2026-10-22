# @s = 기본 공격에 맞은 몹. #dmg 에 방어력의 #operaPm‰(30퍼센트)를 더함(치명타면 그만큼 커짐), 횟수 -1
scoreboard players remove #operaN itv 1
scoreboard players operation #t1 itv = @a[tag=player,limit=1] def
scoreboard players operation #t1 itv *= #operaPm tmp
scoreboard players operation #t1 itv /= #1000 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv *= @a[tag=player,limit=1] critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #t1 itv /= #100 tmp
scoreboard players operation #dmg tmp += #t1 itv
