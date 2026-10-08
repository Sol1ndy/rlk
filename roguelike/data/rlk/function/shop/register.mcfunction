# 상점 상수/스테이지 초기화 (load 에서 호출)
# 사용법: 슬롯 추가  = execute positioned <x> <y> <z> run function rlk:shop/add_slot   (그 칸에 윤나는 안산암+유리가 놓이고 아이템이 진열됨)
#         리롤 버튼 = execute positioned <x> <y> <z> run function rlk:shop/set_reroll
#         슬롯 제거 = function rlk:shop/remove_nearest (또는 안산암/유리를 부수면 자동 제거)
#         구매/리롤 = 버튼을 조준(글씨 커짐)하고 좌클릭
scoreboard objectives add stage dummy
execute unless score cur stage matches 1.. run scoreboard players set cur stage 1
# (쓰지 않음) 예전의 스테이지별 등급 가중치. 지금은 items/register 의 챕터별 확률(rar_wt)을 씀
data modify storage rlk:shop wt set value {s1:{t1:45,t2:80,t3:95},s2:{t1:35,t2:70,t3:90},s3:{t1:25,t2:55,t3:80},s4:{t1:12,t2:37,t3:67},s5:{t1:3,t2:18,t3:50}}
# 등급별 구매가
data modify storage rlk:shop buyprice set value {common:300,rare:500,epic:800,legendary:1400,mythic:2500}
# 리롤 비용
data modify storage rlk:shop reroll_cost set value 600
# 슬롯 좌표 목록(최초만 초기화)
execute unless data storage rlk:shop slots run data modify storage rlk:shop slots set value []
