# io.src / io.id / io.slot 기준으로 @s 의 슬롯에 아이템 배치
function rlk:items/build_display
# 설명 판 번호(리로드마다 +1): 인벤 정리(player/inv/place_check)가 판이 다른 아이템을 새 설명으로 다시 만든다
data modify storage rlk:io ver set from storage rlk:items ver
function rlk:items/place_macro with storage rlk:io
