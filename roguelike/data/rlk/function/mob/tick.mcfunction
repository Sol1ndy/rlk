execute if entity @s[tag=rlk_raiden,scores={rdDeath=1}] run return 0
# @s = 몹, at @s
# 클릭 실드 유지: 몹으로 가는 클릭을 바닐라 타격 대신 실드가 받음(빨간 플래시는 실제 데미지 때만)
execute unless score #bowChg tmp matches 1 run function rlk:mob/shield_ensure
execute if score @s stunT matches 1.. run scoreboard players remove @s stunT 1
execute if score @s stunT matches 0 run function rlk:mob/unstun
# 체력/최대체력 (스코어 mhpC / mhpM)
execute unless score @s mhpM matches 1.. run function rlk:mob/hp_init
# 바닐라 피해 감지(바닐라 체력은 1024 고정)
execute store result score #vh tmp run data get entity @s Health 100
execute if score #vh tmp matches 1..102399 run function rlk:mob/vanilla_hit
scoreboard players operation #h tmp = @s mhpC
scoreboard players operation #mh tmp = @s mhpM
execute if score #mh tmp matches ..0 run scoreboard players set #mh tmp 1
# 전경 바 폭 = Health/maxHealth × 1.6
scoreboard players operation #w tmp = #h tmp
scoreboard players operation #w tmp *= #hb80 tmp
scoreboard players operation #w tmp /= #mh tmp
execute if score #w tmp matches ..0 run scoreboard players set #w tmp 0
execute on passengers if entity @s[tag=rlk_hb_fg] store result entity @s transformation.scale[0] float 0.01 run scoreboard players get #w tmp
# 숫자 (H/maxH)
execute store result storage rlk:hb h int 1 run scoreboard players get #h tmp
execute store result storage rlk:hb mh int 1 run scoreboard players get #mh tmp
execute store result storage rlk:hb lv int 1 run scoreboard players get @s mlv
execute on passengers if entity @s[tag=rlk_hb_num] run function rlk:mob/hb_num with storage rlk:hb
# 레벨(바 위의 큰 글자): 바뀌었을 때만
scoreboard players operation #lvNow tmp = @s mlv
execute unless score #lvNow tmp matches 1.. run scoreboard players set #lvNow tmp 1
execute store result storage rlk:hb lv int 1 run scoreboard players get #lvNow tmp
execute on passengers if entity @s[tag=rlk_hb_lv] unless score @s mlv = #lvNow tmp run function rlk:mob/hb_lv with storage rlk:hb
# 원소 부착/반응 처리 (상태가 있을 때만)
execute if score @s elAct matches 1.. run function rlk:element/tick
