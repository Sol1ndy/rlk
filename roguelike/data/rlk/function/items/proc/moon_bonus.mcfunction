# @s = 맞는 몹. 플레이어의 생명의 계약 % × 0.3 (최대 #cmoonMax)
execute as @a[tag=player,limit=1] run function rlk:player/bol/pct
scoreboard players operation #t1 itv = #bolNow tmp
scoreboard players operation #t1 itv *= #st3 tmp
scoreboard players operation #t1 itv /= #st10 tmp
execute if score #t1 itv > #cmoonMax tmp run scoreboard players operation #t1 itv = #cmoonMax tmp
scoreboard players operation #eb eng += #t1 itv
