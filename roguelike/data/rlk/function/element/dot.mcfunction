# 반응 피해 1회를 @s 에게 (입력: #dmg, #elem). 원소 부착 없음, 증폭 없음
scoreboard players set #crit tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elU tmp 0
scoreboard players set #icd tmp 0
scoreboard players set #tfm tmp 1
scoreboard players set #skillDmg tmp 0
execute if entity @s[type=minecraft:player] run return run function rlk:player/hurt_elem
function rlk:combat/apply
