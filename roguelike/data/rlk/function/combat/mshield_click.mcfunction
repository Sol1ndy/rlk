# @s = 클릭된 실드, at @s. 클릭한(가장 가까운) 플레이어의 공격으로 처리
data remove entity @s attack
execute as @a[tag=player,limit=1] at @s run function rlk:combat/on_attack
