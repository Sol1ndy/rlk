# 캐릭터 매 틱 (@s = 플레이어): 재사용 대기 / 원소 에너지 표시값 / 캐릭터별 처리
execute unless score @s energy matches 0.. run function rlk:char/player_init
execute if score @s skillCd matches 1.. run scoreboard players remove @s skillCd 1
execute if score @s burstCd matches 1.. run scoreboard players remove @s burstCd 1
execute if score @s energy > #burstCost100 tmp run scoreboard players operation @s energy = #burstCost100 tmp
scoreboard players operation @s energyPt = @s energy
scoreboard players operation @s energyPt /= #100 tmp
execute unless items entity @s inventory.0 minecraft:player_head[minecraft:custom_data~{rlk_char:1b}] run function rlk:char/place_info
execute if data storage rlk:chars cur.info.extra.lore[0] unless items entity @s inventory.2 minecraft:paper[minecraft:custom_data~{rlk_ext:1b}] run function rlk:char/place_info
execute if data storage rlk:chars cur.info.passive[0] unless items entity @s inventory.1 minecraft:paper[minecraft:custom_data~{rlk_pas:1b}] run function rlk:char/place_info
execute if score #charN tmp matches 1 at @e[tag=rlk_body,limit=1] run function rlk:char/lumine/tick
execute if score #charN tmp matches 2 at @e[tag=rlk_body,limit=1] run function rlk:char/yoimiya/tick
# 활: 조준(차지) 상태 · 예약된 화살
execute if score #wType tmp matches 2 at @e[tag=rlk_body,limit=1] run function rlk:char/bow/tick
execute unless score #wType tmp matches 2 run scoreboard players set #bowChg tmp 0
execute if score #charN tmp matches 3 at @e[tag=rlk_body,limit=1] run function rlk:char/skirk/tick
execute unless score #charN tmp matches 3 run scoreboard players set #skMode tmp 0
# 원소폭발 시전 동작
execute if score @s buT matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:char/burst_wind_tick
# 일반 공격 모션의 나머지 조각
execute if score @s fxT matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:char/fx/tick
# 근접 공통: 두 번 치는 타의 두 번째 참격
execute if score @s naQ matches 1.. at @e[tag=rlk_body,limit=1] run function rlk:char/melee/q_tick
execute if score #charN tmp matches 4 at @e[tag=rlk_body,limit=1] run function rlk:char/clorinde/tick
execute unless score #charN tmp matches 4 run scoreboard players set #clShoot tmp 0
execute if score #charN tmp matches 5 at @e[tag=rlk_body,limit=1] run function rlk:char/arlecchino/tick
execute if score #charN tmp matches 6 at @e[tag=rlk_body,limit=1] run function rlk:char/navia/tick
execute if score #charN tmp matches 7 at @e[tag=rlk_body,limit=1] run function rlk:char/ronova/tick
execute if score #charN tmp matches 8 at @e[tag=rlk_body,limit=1] run function rlk:char/nefer/tick
