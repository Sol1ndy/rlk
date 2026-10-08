# 예리한 얼음 (@s = 플레이어, combat/find 에서 기본 공격 피해 계산 직후): 얼음 원소 피해로 전환(원소 부여보다 우선) + 공격력의 80%만큼 피해 증가
scoreboard players set #elem tmp 4
scoreboard players set #c tmp 80
scoreboard players operation #pb tmp = @s atk
scoreboard players operation #pb tmp *= #c tmp
scoreboard players operation #pb tmp /= #100 tmp
execute if score #crit tmp matches 1 run scoreboard players operation #pb tmp *= @s critDamage
execute if score #crit tmp matches 1 run scoreboard players operation #pb tmp /= #100 tmp
scoreboard players operation #dmg tmp += #pb tmp
