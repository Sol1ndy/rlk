scoreboard players operation #enAdd tmp = @s pcVal
execute as @p[tag=player] run function rlk:char/energy_add
# 각인 순환 4개: 입자를 얻을 때마다 스킬 재사용 대기 감소
execute if score cycle engN matches 4.. run scoreboard players operation #cut eng = #cycleCut tmp
execute if score cycle engN matches 4.. as @p[tag=player] run function rlk:engravings/cd_cut
execute unless score #k220 snd matches 1 run function rlk:snd/f243
particle minecraft:end_rod ~ ~1 ~ 0.15 0.2 0.15 0.01 2
kill @s
