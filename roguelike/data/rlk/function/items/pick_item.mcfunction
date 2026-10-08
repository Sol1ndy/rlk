# 등급 #g(0 일반,1 레어,2 유니크,3 레전더리,4 신화)의 아이템을 무중복으로 1개 선택 → storage rlk:pick pid (없으면 pid 없음)
# rlk:pick picked 목록(이번 추첨에서 이미 뽑힌 것)과 플레이어 보유 목록에 있는 것은 제외
data modify storage rlk:pick grarr set value ["common","rare","epic","legendary","mythic"]
execute store result storage rlk:pick gi int 1 run scoreboard players get #g tmp
function rlk:items/pick_rar with storage rlk:pick
function rlk:items/pick_cand with storage rlk:pick
scoreboard players set #tries tmp 12
scoreboard players set #pok tmp 0
data remove storage rlk:pick pid
data remove storage rlk:pick cid
function rlk:items/pick_loop
