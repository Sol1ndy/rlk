# @s = 맞는 몹. 플레이어의 생명의 계약 % × #cmoonRate‰ (최대 #cmoonMax, 둘 다 강화 단계로 조정)
execute as @a[tag=player,limit=1] run function rlk:player/bol/pct
scoreboard players operation #t1 itv = #bolNow tmp
scoreboard players operation #t1 itv *= #cmoonRate tmp
scoreboard players operation #t1 itv /= #1000 tmp
execute if score #t1 itv > #cmoonMax tmp run scoreboard players operation #t1 itv = #cmoonMax tmp
scoreboard players operation #eb eng += #t1 itv
