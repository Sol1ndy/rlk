# 반응의 출처 = 플레이어 (@s = 플레이어). 반응 기준 #rBase = 공격력 × #reactBase%
scoreboard players operation #rBase tmp = @s atk
scoreboard players operation #rBase tmp *= #reactBase tmp
scoreboard players operation #rBase tmp /= #100 tmp
execute if score #rBase tmp matches ..0 run scoreboard players set #rBase tmp 1
# 원소 마스터리 보정(%) — 원신 공식: 격변 16EM/(EM+2000), 증폭 2.78EM/(EM+1400), 촉진·발산 5EM/(EM+1200), 결정 4.44EM/(EM+1400)
scoreboard players operation #em tmp = @s elemMastery
execute if score #em tmp matches ..-1 run scoreboard players set #em tmp 0
scoreboard players set #c tmp 1600
scoreboard players operation #emT tmp = #em tmp
scoreboard players operation #emT tmp *= #c tmp
scoreboard players operation #t tmp = #em tmp
scoreboard players add #t tmp 2000
scoreboard players operation #emT tmp /= #t tmp
scoreboard players set #c tmp 278
scoreboard players operation #emA tmp = #em tmp
scoreboard players operation #emA tmp *= #c tmp
scoreboard players operation #t tmp = #em tmp
scoreboard players add #t tmp 1400
scoreboard players operation #emA tmp /= #t tmp
scoreboard players set #c tmp 444
scoreboard players operation #emC tmp = #em tmp
scoreboard players operation #emC tmp *= #c tmp
scoreboard players operation #emC tmp /= #t tmp
scoreboard players set #c tmp 500
scoreboard players operation #emD tmp = #em tmp
scoreboard players operation #emD tmp *= #c tmp
scoreboard players operation #t tmp = #em tmp
scoreboard players add #t tmp 1200
scoreboard players operation #emD tmp /= #t tmp
