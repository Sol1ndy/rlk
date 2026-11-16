# io.id 의 아이템 정보를 불러와 표시용 이름/모델을 만든다 (macro: id)
data remove storage rlk:io src
$data modify storage rlk:io src set from storage rlk:items registry.$(id)
# 별 · 능력치 배율 · 설명 사본은 io.id 로 찾는다
$data modify storage rlk:io id set value "$(id)"
data remove storage rlk:io clickdrop
function rlk:items/build_display
