# 「검신합일」 반격 (@s = 플레이어, at 몸, hw_due): 몸에서 가장 가까운 12칸 안의 적(rlk_mob, 보스 몸체 포함) 하나에게
# 공격력의 #hwCtrCoef % 번개 원소 피해(아이템 효과: #sub itv 1). 대상이 없으면 재사용 대기를 쓰지 않는다. 무적인 보스 몸체
# (rlk_mb_inv: 연출 · 유령 · 연참 동안)는 대상이 아니다(맞지 않는 몸에 반격 · 재사용 대기를 쓰지 않음)
scoreboard players set #hwCtrQ itv 0
execute if score #hwCtrCd itv matches 1.. run return 0
tag @e[tag=rlk_mob,tag=!rlk_mb_inv,distance=..12,sort=nearest,limit=1] add rlk_hw_t
execute unless entity @e[tag=rlk_hw_t,limit=1] run return 0
# 재사용 대기: #hwCtrCd 1 인 동안 새 예약 없음(player/take_damage · dash_iframe 의 줄), #hwCtrEnd = 끝나는 시각
scoreboard players set #hwCtrCd itv 1
scoreboard players operation #hwCtrEnd itv = #hwNow itv
scoreboard players operation #hwCtrEnd itv += #hwCtrCdT tmp
execute as @e[tag=rlk_hw_t] at @s facing entity @e[tag=rlk_body,limit=1] feet run function rlk:items/proc/hw_ctr_fx
execute store result storage rlk:tune m_sword_hwamu.coef int 1 run scoreboard players get #hwCtrCoef tmp
function rlk:char/dmg_calc with storage rlk:tune m_sword_hwamu
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hw_t] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hw_t] remove rlk_hw_t
scoreboard players set #sub itv 0
execute unless score #k354 snd matches 1 run function rlk:snd/f424
execute unless score #k355 snd matches 1 run function rlk:snd/f425
function rlk:char/after_hit
