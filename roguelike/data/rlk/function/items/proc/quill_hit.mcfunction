# @s = 예약 표식, at @s. 가장 가까운 적(2.5칸)에게 공격력의 #quillCoef% 얼음 원소 추가 피해(원소 부착 없음, 계수는 강화 단계로 조정)
execute store result storage rlk:tune m_ice_quill.coef int 1 run scoreboard players get #quillCoef tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:tune m_ice_quill
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 4
scoreboard players set #elU tmp 0
scoreboard players set #quillHit itv 1
execute as @e[tag=rlk_mob,distance=..2.5,sort=nearest,limit=1] at @s run function rlk:items/proc/quill_fx
scoreboard players set #quillHit itv 0
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
kill @s
scoreboard players set #sub itv 0
