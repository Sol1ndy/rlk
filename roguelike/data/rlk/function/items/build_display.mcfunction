# src(=io.src), io.id 로부터 io.name / io.lore / io.item / io.model 구성 (지급/배치/드롭/상점 공용)
data modify storage rlk:io color set value "white"
data modify storage rlk:io rlabel set value "ITEM"
data modify storage rlk:io tlabel set value ""
data modify storage rlk:io rarity set from storage rlk:io src.rarity
data modify storage rlk:io type set from storage rlk:io src.type
function rlk:items/resolve_rarity with storage rlk:io
data modify storage rlk:io nm set from storage rlk:io src.name
function rlk:items/set_name with storage rlk:io
data modify storage rlk:io lore set value []
function rlk:items/build_lore
data modify storage rlk:io item set from storage rlk:io src.item
# 모델: 기본 = 바닐라 아이템 모양 / use_models 켜짐 = rlk:<id> / 정의에 model 이 있으면 그 값
data modify storage rlk:io model set from storage rlk:io src.item
execute if data storage rlk:config {use_models:1b} run function rlk:items/set_model with storage rlk:io
execute if data storage rlk:io src.model run data modify storage rlk:io model set from storage rlk:io src.model
