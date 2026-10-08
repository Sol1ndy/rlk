# @s = 우클릭된 실드, at @s. 클릭한(가장 가까운) 플레이어의 우클릭으로 처리
data remove entity @s interaction
execute as @a[tag=player,limit=1] at @s run function rlk:combat/rclick_do
