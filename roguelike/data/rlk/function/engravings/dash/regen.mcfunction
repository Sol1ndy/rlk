# 질주 2개: 닷지 재사용 대기 = 기본 × (100 - #dashEngSpd) / 100 (최소 1틱)
scoreboard players set #t1 eng 100
scoreboard players operation #t1 eng -= #dashEngSpd tmp
scoreboard players operation #dashCoolT tmp *= #t1 eng
scoreboard players operation #dashCoolT tmp /= #100 tmp
execute if score #dashCoolT tmp matches ..0 run scoreboard players set #dashCoolT tmp 1
