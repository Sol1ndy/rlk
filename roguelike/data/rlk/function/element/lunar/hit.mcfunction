# 달 피해 한 번 (@s = 몹, at @s). 입력 #lnB(기본 피해) · #lnEl(원소 3 번개 / 7 풀 / 5 바위) · #lnT(1 달 감전 / 2 달 개화 / 3 달 결정)
execute as @a[tag=player,limit=1] run function rlk:element/lunar/calc
scoreboard players set #elem tmp 0
scoreboard players operation #elem tmp = #lnEl tmp
scoreboard players set #elU tmp 0
scoreboard players set #icd tmp 0
scoreboard players set #tfm tmp 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #lunar tmp 1
function rlk:combat/apply
scoreboard players set #lunar tmp 0
function rlk:element/lunar/count
