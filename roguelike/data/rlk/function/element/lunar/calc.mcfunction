# 달 피해 계산 (@s = 플레이어). 입력 #lnB = 기본 피해. 출력 #dmg #crit
# × (100 + 기본 피해 보너스: 네페르 EM × 0.0175%, 최대 14%) × (100 + 600 × EM / (EM + 2000))% × (100 + #lnBuff)% , 치명타
scoreboard players operation #em tmp = @s elemMastery
execute if score #em tmp matches ..-1 run scoreboard players set #em tmp 0
scoreboard players operation #dmg tmp = #lnB tmp
# 네페르 고유 특성: 기본 피해 +EM × 0.0175% (만분율, 최대 1400)
scoreboard players set #lb tmp 0
execute if score #charN tmp matches 8 run scoreboard players operation #lb tmp = #em tmp
execute if score #charN tmp matches 8 run scoreboard players operation #lb tmp *= #c175 tmp
execute if score #charN tmp matches 8 run scoreboard players operation #lb tmp /= #100 tmp
execute if score #lb tmp matches 1401.. run scoreboard players set #lb tmp 1400
scoreboard players add #lb tmp 10000
scoreboard players operation #dmg tmp *= #lb tmp
scoreboard players operation #dmg tmp /= #10000 tmp
# 원소 마스터리: 600 × EM / (EM + 2000) %
scoreboard players operation #le tmp = #em tmp
scoreboard players operation #le tmp *= #c600 tmp
scoreboard players operation #t tmp = #em tmp
scoreboard players add #t tmp 2000
scoreboard players operation #le tmp /= #t tmp
scoreboard players add #le tmp 100
scoreboard players operation #dmg tmp *= #le tmp
scoreboard players operation #dmg tmp /= #100 tmp
# 달 피해 보너스(콜롬비나 원소폭발 등)
scoreboard players set #t tmp 100
scoreboard players operation #t tmp += #lnBuff itv
scoreboard players operation #dmg tmp *= #t tmp
scoreboard players operation #dmg tmp /= #100 tmp
# 치명타
execute store result score #rng tmp run random value 1..100
scoreboard players set #crit tmp 0
execute if score #rng tmp <= @s critChance run scoreboard players set #crit tmp 1
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #dmg tmp /= #100 tmp
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
