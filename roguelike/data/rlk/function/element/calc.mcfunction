# macro: m(%). 격변 반응 피해 #rdmg = 반응 기준(#rBase) × m% × (1 + 원소 마스터리 보정 #emT%)
$scoreboard players set #rdmg tmp $(m)
scoreboard players operation #rdmg tmp *= #rBase tmp
scoreboard players operation #rdmg tmp /= #100 tmp
scoreboard players set #t tmp 100
scoreboard players operation #t tmp += #emT tmp
scoreboard players operation #rdmg tmp *= #t tmp
scoreboard players operation #rdmg tmp /= #100 tmp
execute if score #rdmg tmp matches ..0 run scoreboard players set #rdmg tmp 1
