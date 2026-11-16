# 2챕터 몹 점수(tools/build_ch2_mobs.py): 무리 · 대열 번호, 역할, 타이머, 가속 주기, 나이
scoreboard objectives add c2G dummy
scoreboard objectives add c2R dummy
scoreboard objectives add c2T dummy
scoreboard objectives add c2T2 dummy
scoreboard objectives add c2H dummy
scoreboard objectives add c2Age dummy
# 피해(원피해) · 예고(틱) · 간격(틱) · 뛰기 간격 · 북 중단 · 경직 · 넉백(칸/틱 x1000) · 창병 회전(0.01°/틱) · 연쇄 방전(최대 체력 %)
scoreboard players set #c2D_ns tmp 15
scoreboard players set #c2D_sl tmp 12
scoreboard players set #c2D_ss tmp 6
scoreboard players set #c2D_sp tmp 16
scoreboard players set #c2W_ns tmp 12
scoreboard players set #c2W_sl tmp 10
scoreboard players set #c2W_ss tmp 20
scoreboard players set #c2W_sp tmp 20
scoreboard players set #c2Cd_ns tmp 36
scoreboard players set #c2Cd_sl tmp 50
scoreboard players set #c2Cd_ss tmp 40
scoreboard players set #c2Cd_sp tmp 60
scoreboard players set #c2Hop_sl tmp 24
scoreboard players set #c2Hop_ss tmp 11
scoreboard players set #c2DrI tmp 40
scoreboard players set #c2Stun tmp 5
scoreboard players set #c2KB tmp 420
scoreboard players set #c2Turn tmp 450
scoreboard players set #c2TurnN tmp -450
scoreboard players set #c2ZapS tmp 100
scoreboard players set #c2ZapL tmp 20
scoreboard players set #c2c1000 tmp 1000
scoreboard players set #c2c100 tmp 100
scoreboard players set #c2c12 tmp 12
scoreboard players set #c2c2 tmp 2
scoreboard players set #c2c4 tmp 4
scoreboard players set #c2c3 tmp 3
scoreboard players set #c2c24 tmp 24
scoreboard players add #c2PackC tmp 0
execute unless score #c2K1 tmp matches -2147483648.. run scoreboard players set #c2K1 tmp -1000
execute unless score #c2K2 tmp matches -2147483648.. run scoreboard players set #c2K2 tmp -1000
execute unless score #c2Kq tmp matches -2147483648.. run scoreboard players set #c2Kq tmp -1000
