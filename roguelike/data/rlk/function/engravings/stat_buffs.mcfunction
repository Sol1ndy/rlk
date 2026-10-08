# @s = 플레이어 (2틱마다)
execute if score treasure engN matches 5.. run function rlk:engravings/treasure/atk
execute if score berserk engN matches 6.. if score @s berT matches 1.. run scoreboard players operation @s atkSpeed += #berSpd tmp
execute if score coop engN matches 4.. if score #coopT eng matches 1.. run scoreboard players operation @s atkPct += #coopAtk tmp
execute if score spirit engN matches 4.. if score #spiritT eng matches 1.. run scoreboard players operation @s atkPct += #spiritAtk tmp
# 반석 4개: 결정 방어막을 얻은 뒤 그 원소의 피해 보너스
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 1 run scoreboard players operation @s pyroBonus += #petraDmg tmp
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 2 run scoreboard players operation @s hydroBonus += #petraDmg tmp
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 3 run scoreboard players operation @s electroBonus += #petraDmg tmp
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 4 run scoreboard players operation @s cryoBonus += #petraDmg tmp
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 5 run scoreboard players operation @s geoBonus += #petraDmg tmp
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 6 run scoreboard players operation @s anemoBonus += #petraDmg tmp
execute if score petra engN matches 4.. if score #petraT eng matches 1.. if score #petraEl eng matches 7 run scoreboard players operation @s dendroBonus += #petraDmg tmp
# 계약 2개: 생명의 계약이 있는 동안 공격력
execute if score pact engN matches 2.. if score @s bol matches 1.. run scoreboard players operation @s atkPct += #pactAtk tmp
# 만월 4개: 달 반응 뒤 원소 마스터리
execute if score fullmoon engN matches 4.. if score #fmT eng matches 1.. run scoreboard players operation @s elemMastery += #fmEm tmp
