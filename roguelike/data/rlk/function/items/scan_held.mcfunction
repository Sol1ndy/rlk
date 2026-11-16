# 빠른 스캔 (@s = 플레이어, items/scan_fast 의 조건일 때): order 의 id 를 중복 없이 하나씩(items/scan_body = 전체 순회의 한 id 와 같은 일),
# 그 뒤 지난 스캔에서 가졌는데 이번에 세지 않은 id 의 it_ 를 0 으로(전체 순회라면 개수 0 으로 적었을 것)
data modify storage rlk:scan seen set value {}
data modify storage rlk:scan ids set from storage rlk:pinv order
function rlk:items/scan_hloop
data modify storage rlk:scan ids set from storage rlk:scan hprev
function rlk:items/scan_zloop
