# 원소폭발 아이템: 이름 = "(이름) - [게이지] 현재/필요pt". 재사용 대기 중에는 개수 = 남은 초
scoreboard players operation @s buShown = #bk tmp
clear @s *[minecraft:custom_data~{rlk_ui:{role:"burst"}}]
data modify storage rlk:chars it set from storage rlk:chars cur.burst
execute if score #charN tmp matches 3 if score @s skM matches 1.. run data modify storage rlk:chars it.name set value "극악기 · 진"
data modify storage rlk:chars it.bar set from storage rlk:hud en
execute store result storage rlk:chars it.e int 1 run scoreboard players get @s energyPt
scoreboard players operation #bn tmp = #bs tmp
execute if score #bn tmp matches ..0 run scoreboard players set #bn tmp 1
execute store result storage rlk:chars it.n int 1 run scoreboard players get #bn tmp
# 에너지가 가득 차고 재사용 대기가 끝났으면 반짝임
data modify storage rlk:chars it.glint set value "false"
execute if score @s energy >= #burstCost100 tmp if score #bs tmp matches 0 run data modify storage rlk:chars it.glint set value "true"
execute if score #charN tmp matches 3 run function rlk:char/skirk/burst_glint
execute if score #bs tmp matches 0 run function rlk:char/burst_item_ready with storage rlk:chars it
execute if score #bs tmp matches 1.. run function rlk:char/burst_item_cd with storage rlk:chars it
