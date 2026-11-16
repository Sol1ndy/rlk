# 2단계 · 1단계 패링 (#parT tmp 2 / 1; player/take_damage 의 원소 반응 뒤 — 격변 반응 피해도 함께 줄어듦): #dmgIn × 남기는 % / 100, 최소 1
execute if score #parT tmp matches 2 run scoreboard players operation #dmgIn tmp *= #parKeep2 tmp
execute if score #parT tmp matches 1 run scoreboard players operation #dmgIn tmp *= #parKeep1 tmp
scoreboard players operation #dmgIn tmp /= #100 tmp
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
