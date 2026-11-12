# 「홍련일섬」 베기 (@s = 플레이어, at 몸, hw_due: 시전 #hwSlDelay 틱 뒤): 20칸 안의 모든 적(rlk_mob, 보스 몸체 포함)에게 한 번씩
# 공격력의 #hwSlCoef % 번개 원소 피해(아이템 효과: #sub itv 1, 치명타 판정은 한 번)
scoreboard players set #hwSlQ itv 0
tag @e[tag=rlk_mob,distance=..20] add rlk_hw_s
execute unless entity @e[tag=rlk_hw_s,limit=1] run return 0
execute as @e[tag=rlk_hw_s] at @s run function rlk:items/proc/hw_slash_fx
execute store result storage rlk:tune m_sword_hwamu.coef int 1 run scoreboard players get #hwSlCoef tmp
function rlk:char/dmg_calc with storage rlk:tune m_sword_hwamu
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players set #sub itv 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_hw_s] at @s run function rlk:combat/apply_reset
tag @e[tag=rlk_hw_s] remove rlk_hw_s
scoreboard players set #sub itv 0
execute unless score #k357 snd matches 1 run function rlk:snd/f427
execute unless score #k358 snd matches 1 run function rlk:snd/f428
function rlk:char/after_hit
