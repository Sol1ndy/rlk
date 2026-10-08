# @s = 몹. 예약된 반응 피해(과부하·초전도 = rxDmg, 감전 = ecDmg)를 #thunderDmg% 늘린다
scoreboard players operation #t1 eng = #thunderDmg tmp
scoreboard players add #t1 eng 100
execute if score #rx tmp matches 3..4 run scoreboard players operation @s rxDmg *= #t1 eng
execute if score #rx tmp matches 3..4 run scoreboard players operation @s rxDmg /= #100 tmp
execute if score #rx tmp matches 5 run scoreboard players operation @s ecDmg *= #t1 eng
execute if score #rx tmp matches 5 run scoreboard players operation @s ecDmg /= #100 tmp
# 4개: 스킬 재사용 대기 감소(내부 쿨타임 #thunderIcd 틱)
execute unless score thunder engN matches 4.. run return 0
execute if score #thunderT eng matches 1.. run return 0
scoreboard players operation #thunderT eng = #thunderIcd tmp
scoreboard players operation #cut eng = #thunderCut tmp
execute as @a[tag=player,limit=1] run function rlk:engravings/cd_cut
