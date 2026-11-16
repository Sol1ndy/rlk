# @s = 예약 표식, at @s. 뇌벌 악요의 눈 협동 공격: 반경 3칸에 공격력의 #eyeCoef% 번개 원소 피해 (강화 단계로 조정, 치명타 판정 있음, 스킬 피해로 치지 않음)
execute store result storage rlk:tune m_stormy_eye.coef int 1 run scoreboard players get #eyeCoef tmp
execute as @a[tag=player,limit=1] run function rlk:char/dmg_calc with storage rlk:tune m_stormy_eye
scoreboard players set #sub itv 1
scoreboard players set #skillDmg tmp 0
scoreboard players set #stunHit tmp 0
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players set #icd tmp 1
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_mob,distance=..3] at @s run function rlk:combat/apply_reset
# 연출: 위에서 내리꽂는 보랏빛 번개
particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:1.5f} ~ ~2.2 ~ 0.08 1.6 0.08 0 30
particle minecraft:electric_spark ~ ~0.8 ~ 0.9 0.5 0.9 0.4 25
particle minecraft:dust{color:[0.6f,0.33f,0.91f],scale:1.1f} ~ ~0.3 ~ 1.4 0.1 1.4 0 24
execute unless score #k126 snd matches 1 run function rlk:snd/f134
execute unless score #k127 snd matches 1 run function rlk:snd/f135
execute as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:char/after_hit
kill @s
scoreboard players set #sub itv 0
