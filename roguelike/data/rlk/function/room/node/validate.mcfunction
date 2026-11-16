# rlk:room next 에서 지금 쓸모없는 노드 빼기: 8 나무뿌리(기적을 이미 받음), 12 보유 칸(18칸). 다 빠지면 [3] 골드
data modify storage rlk:room vq set from storage rlk:room next
data modify storage rlk:room next set value []
function rlk:room/node/validate_loop
execute unless data storage rlk:room next[0] run data modify storage rlk:room next set value [3]
# 상점만 남으면 골드를 붙인다(상점은 혼자 나오지 않음)
execute unless data storage rlk:room next[1] if data storage rlk:room {next:[4]} run data modify storage rlk:room next append value 3
