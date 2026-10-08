# 선택 확정: pid=cid, picked에 추가, 완료 플래그
data modify storage rlk:pick pid set from storage rlk:pick cid
data modify storage rlk:pick picked append from storage rlk:pick cid
scoreboard players set #pok tmp 1
