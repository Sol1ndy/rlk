# 등급별 아이템 목록 버킷 생성 (register 에서 호출). rlk:items byrar.{common,rare,epic,legendary,mythic}
# 추첨 제외 목록(변신 등 특별 루트 전용 아이템)
data modify storage rlk:items box_exclude set value ["sword_kirion","demonomicon"]
data modify storage rlk:items byrar set value {common:[],rare:[],epic:[],legendary:[],mythic:[]}
data modify storage rlk:rb ids set from storage rlk:items ids
function rlk:items/rb_loop
