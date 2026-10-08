# 밤 사냥 (@s = 플레이어, at 몸). 밤 순찰 중에 다시 누르면 밤 꿰뚫기
# 밤 순찰 중: 스킬 아이템 좌클릭(#skBtn 1) = 수렵(자동 연사 켜기/끄기), 우클릭 = 밤 꿰뚫기
execute if score @s clNV matches 1.. if score #skBtn tmp matches 1 run return run function rlk:char/clorinde/auto_toggle
execute if score @s clNV matches 1.. run return run function rlk:char/clorinde/lunge
execute if score @s skillCd matches 1.. run return run function rlk:char/deny {t:"원소전투 스킬 재사용 대기 중"}
scoreboard players operation @s skillCd = #skillCdT tmp
function rlk:char/cd_reduce
scoreboard players operation @s clNV = #clDur tmp
scoreboard players set @s clPcN 0
scoreboard players set @s clPcCd 0
scoreboard players set #clShoot tmp 1
scoreboard players set @s clLCd 6
scoreboard players set @s comboStep 0
execute as @e[tag=rlk_av,limit=1] run swing @s mainhand
playsound minecraft:item.crossbow.loading_end master @a ~ ~ ~ 0.9 0.8
playsound minecraft:entity.lightning_bolt.thunder master @a ~ ~ ~ 0.25 2.0
particle minecraft:electric_spark ~ ~1 ~ 0.5 0.7 0.5 0.3 40
particle minecraft:dust{color:[0.77f,0.55f,1.0f],scale:1.5f} ~ ~1 ~ 0.6 0.8 0.6 0 20
function rlk:items/hook/on_cast_skill
function rlk:combat/on_skill
