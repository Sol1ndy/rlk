# 질주 2개: 닷지 재사용 대기 = 기본 × (100 - #dashEngSpd) / 100, 반올림(최소 1틱): 18 → 14, 공격을 피한 닷지 12 → 10
scoreboard players set #t1 eng 100
scoreboard players operation #t1 eng -= #dashEngSpd tmp
scoreboard players operation #dashCoolT tmp *= #t1 eng
scoreboard players add #dashCoolT tmp 50
scoreboard players operation #dashCoolT tmp /= #100 tmp
execute if score #dashCoolT tmp matches ..0 run scoreboard players set #dashCoolT tmp 1
scoreboard players operation #dashCoolHitT tmp *= #t1 eng
scoreboard players add #dashCoolHitT tmp 50
scoreboard players operation #dashCoolHitT tmp /= #100 tmp
execute if score #dashCoolHitT tmp matches ..0 run scoreboard players set #dashCoolHitT tmp 1
