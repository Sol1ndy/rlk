# 각인별 아이템 목록 rlk:engravings byeng.<각인 id> = [아이템 id...] (load 에서 items/register 다음에). 나무뿌리 기적이 쓴다
data modify storage rlk:engravings byeng set value {}
data modify storage rlk:engravings bq set from storage rlk:items ids
function rlk:engravings/byeng_loop
