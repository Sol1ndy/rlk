# io.id 의 아이템 정보를 불러와 표시용 이름/모델을 만든다 (macro: id)
data remove storage rlk:io src
$data modify storage rlk:io src set from storage rlk:items registry.$(id)
data remove storage rlk:io clickdrop
function rlk:items/build_display
