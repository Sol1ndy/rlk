# macro: id → #enh tmp = 그 아이템의 강화 단계 (rlk:pinv enh.<id>, 없으면 그대로 0)
$execute if data storage rlk:pinv enh.$(id) store result score #enh tmp run data get storage rlk:pinv enh.$(id)
