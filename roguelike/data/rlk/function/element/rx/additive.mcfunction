# 촉진(번개)/발산(풀): 활성 상태를 소모하지 않고 이번 타격에 추가 피해. macro: m(%), rx
$scoreboard players set #addDmg tmp $(m)
scoreboard players operation #addDmg tmp *= #rBase tmp
scoreboard players operation #addDmg tmp /= #100 tmp
scoreboard players set #t tmp 100
scoreboard players operation #t tmp += #emD tmp
scoreboard players operation #addDmg tmp *= #t tmp
scoreboard players operation #addDmg tmp /= #100 tmp
execute if score #addDmg tmp matches ..0 run scoreboard players set #addDmg tmp 1
$scoreboard players set #rx tmp $(rx)
