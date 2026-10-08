# @s = atkBlock. 우클릭(interaction)만 감지 → 스킬/대쉬. 좌클릭(attack)은 atkStrike 전담이라 흡수/무시
data remove entity @s attack
execute store success score #rc tmp run data remove entity @s interaction
execute if score #rc tmp matches 1 as @a if score @s pid = #mypid tmp at @s run function rlk:combat/rclick_do
