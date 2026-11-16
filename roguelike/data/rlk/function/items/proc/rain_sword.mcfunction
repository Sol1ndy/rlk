# @s = 플레이어, 위치 = 몸. 가장 가까운 적(7칸)에게 물의 검: 공격력의 #rainCoef 퍼센트 물 원소 피해. 본타격의 치명타 여부(#crit)는 보존
scoreboard players operation #rainCd itv = #rainCdT tmp
scoreboard players operation #svCrit itv = #crit tmp
# 피해 계수 = #rainCoef (강화 단계로 조정)
execute store result storage rlk:tune m_rain_sheath.coef int 1 run scoreboard players get #rainCoef tmp
function rlk:char/dmg_calc with storage rlk:tune m_rain_sheath
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 2
scoreboard players set #elU tmp 1000
scoreboard players set #basic itv 0
execute as @e[tag=rlk_mob,distance=..7,sort=nearest,limit=1] at @s run function rlk:items/proc/rain_hit
scoreboard players set #basic itv 1
function rlk:char/after_hit
scoreboard players operation #crit tmp = #svCrit itv
scoreboard players set #sub itv 0
