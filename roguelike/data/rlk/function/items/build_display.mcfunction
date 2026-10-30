# src(=io.src), io.id 로부터 io.name / io.lore / io.item / io.model 구성 (지급/배치/드롭/상점 공용)
data modify storage rlk:io color set value "white"
data modify storage rlk:io rlabel set value "ITEM"
data modify storage rlk:io tlabel set value ""
data modify storage rlk:io rarity set from storage rlk:io src.rarity
data modify storage rlk:io type set from storage rlk:io src.type
function rlk:items/resolve_rarity with storage rlk:io
data modify storage rlk:io nm set from storage rlk:io src.name
# 강화 단계(rlk:pinv enh.<id>, 0~3) → 이름 뒤 별(★ 채움 · ☆ 빔). 캐릭터는 별 없음
scoreboard players set #enh tmp 0
function rlk:items/enh_get with storage rlk:io
execute if score #enh tmp matches 4.. run scoreboard players set #enh tmp 3
execute store result storage rlk:io enh int 1 run scoreboard players get #enh tmp
data modify storage rlk:io sx set value [{text:""}]
execute unless data storage rlk:io {rarity:"character"} run function rlk:items/stars with storage rlk:io
function rlk:items/set_name with storage rlk:io
# 능력치 표시 = 강화 단계 배율(효과량 #fA) 적용 (items/tune)
execute unless data storage rlk:io {rarity:"character"} if data storage rlk:io src.stats run function rlk:items/tune/fac
execute unless data storage rlk:io {rarity:"character"} if data storage rlk:io src.stats run function rlk:items/tune/stats_scale
data modify storage rlk:io lore set value []
function rlk:items/build_lore
data modify storage rlk:io item set from storage rlk:io src.item
# 모델: 기본 = 바닐라 아이템 모양 / use_models 켜짐 = rlk:<id> / 정의에 model 이 있으면 그 값
data modify storage rlk:io model set from storage rlk:io src.item
execute if data storage rlk:config {use_models:1b} run function rlk:items/set_model with storage rlk:io
execute if data storage rlk:io src.model run data modify storage rlk:io model set from storage rlk:io src.model
