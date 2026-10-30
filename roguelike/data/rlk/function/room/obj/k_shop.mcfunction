# 상점 구역 (위치 = 구역 표식 = 바닥 위 한가운데): 가운데 상인 + 진열대 8개(아이템 6 · 회복 소/대). 구매 = 가격표를 조준하고 좌클릭(shop/)
# 진열 자리를 비우고 구덩이는 메운다(구역 크기는 19칸 이상)
fill ~-7 ~ ~-6 ~7 ~3 ~6 minecraft:air
fill ~-7 ~-1 ~-6 ~7 ~-1 ~6 minecraft:polished_andesite replace #rlk:cannon_clear
fill ~-7 ~-1 ~-6 ~7 ~-1 ~6 minecraft:polished_andesite replace minecraft:lava
fill ~-7 ~-1 ~-6 ~7 ~-1 ~6 minecraft:polished_andesite replace minecraft:water
summon minecraft:wandering_trader ~ ~ ~ {Tags:["rlk_room","rlk_pet","rlk_new"],NoAI:1b,Invulnerable:1b,Silent:1b,PersistenceRequired:1b,DespawnDelay:0,Rotation:[180f,0f]}
scoreboard players set #oact tmp 3
scoreboard players set #oarg tmp 0
summon minecraft:marker ~ ~1 ~ {Tags:["rlk_room","rlk_obj","rlk_new"]}
summon minecraft:text_display ~ ~2.75 ~ {Tags:["rlk_room","rlk_olbl","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:[{text:"상인",color:"#6FCF8F",bold:true},{text:"\n진열대의 가격표를 눌러 산다",color:"#D0D0D0",bold:false}],transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
summon minecraft:text_display ~ ~2.4 ~ {Tags:["rlk_room","rlk_ohint","rlk_new"],billboard:"center",alignment:"center",brightness:{sky:15,block:15},shadow:true,background:0,text:{text:""},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute store result score #ogid room run scoreboard players add #ogid room 1
scoreboard players operation @e[tag=rlk_new] ogid = #ogid room
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oact = #oact tmp
scoreboard players operation @e[tag=rlk_new,tag=rlk_obj] oarg = #oarg tmp
tag @e[tag=rlk_new] remove rlk_new
function rlk:shop/node/setup
