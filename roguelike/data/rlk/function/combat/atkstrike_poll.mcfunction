# @s = atkStrike. 좌클릭(attack)=공격, 우클릭(interaction)=스킬/대쉬. 각 원자적 제거
execute store success score #lc tmp run data remove entity @s attack
execute store success score #rc tmp run data remove entity @s interaction
execute if score #lc tmp matches 1 as @a if score @s pid = #mypid tmp at @s run function rlk:combat/on_attack
execute if score #rc tmp matches 1 as @a if score @s pid = #mypid tmp at @s run function rlk:combat/rclick_do
