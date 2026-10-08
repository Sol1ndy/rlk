# 발광 아이템 스폰 + 기록 저장 + UI(정보/버튼) 생성 (at 위치). macro: item, id, model
# Age:-32768 = 자연 소멸(5분) 없음 → 버튼/설명만 남는 일 방지
scoreboard players add #dgid tmp 1
$summon minecraft:item ~ ~0.35 ~ {Tags:["rlk_ditem","rlk_dnew","rlk_dgrp"],Glowing:1b,PickupDelay:32767s,Age:-32768s,Invulnerable:1b,Item:{id:"$(item)",count:1,components:{"minecraft:custom_data":{rlk_ditem:{id:"$(id)"}},"minecraft:item_model":"$(model)"}}}
execute if data storage rlk:io src.prof run data modify entity @e[tag=rlk_ditem,tag=rlk_dnew,limit=1] Item.components."minecraft:profile" set from storage rlk:io src.prof
execute as @e[tag=rlk_dnew] run scoreboard players operation @s dgid = #dgid tmp
# 판매가를 아이템에 저장
execute as @e[tag=rlk_ditem,tag=rlk_dnew] store result score @s dprice run data get storage rlk:io price
# 기록 저장
execute store result storage rlk:ditems key int 1 run scoreboard players get #dgid tmp
function rlk:items/drop_store with storage rlk:ditems
# 아우라(레전더리/신화)
execute if data storage rlk:io {rarity:"legendary"} run tag @e[tag=rlk_ditem,tag=rlk_dnew] add rlk_daura
execute if data storage rlk:io {rarity:"mythic"} run tag @e[tag=rlk_ditem,tag=rlk_dnew] add rlk_daura
# UI 생성
data modify storage rlk:dui name set from storage rlk:io name
data modify storage rlk:dui price set from storage rlk:io price
scoreboard players operation #uigid tmp = #dgid tmp
function rlk:items/spawn_ditem_ui with storage rlk:dui
tag @e[tag=rlk_dnew] remove rlk_dnew
playsound minecraft:entity.item.pickup master @a ~ ~ ~ 0.4 0.6
