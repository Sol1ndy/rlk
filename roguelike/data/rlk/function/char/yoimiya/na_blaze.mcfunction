# 염초 정화의 춤: 기본 공격 화살 → 염초 화살(불 원소, 피해 × #yoiSkMul%)
scoreboard players set #aEl tmp 1
scoreboard players set #aKind tmp 5
scoreboard players operation #dmg tmp *= #yoiSkMul tmp
scoreboard players operation #dmg tmp /= #100 tmp
