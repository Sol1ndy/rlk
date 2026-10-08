# 광역 반응 피해 1명분 (@s = 몹, at @s). #qDmg/#qEl/#qU 에서 매번 복원(대상마다 독립 계산)
scoreboard players operation #dmg tmp = #qDmg tmp
scoreboard players operation #elem tmp = #qEl tmp
scoreboard players operation #elU tmp = #qU tmp
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #icd tmp 0
scoreboard players set #tfm tmp 1
scoreboard players set #skillDmg tmp 0
function rlk:combat/apply
