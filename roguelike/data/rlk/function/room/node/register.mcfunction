# 노드 목록 (load 에서 room/data 다음에 호출). 노드 = 맵 선택지에 붙어 그 맵의 중간 구역 하나를 특수 구역으로 바꾸는 요소
# 키 k<구역 종류(zkind)>: name(이름) · item/model(선택지 · 제목 아이콘) · desc(한 줄 설명) · color
data modify storage rlk:room nodes set value {\
k3:{k:3,name:"골드",item:"minecraft:gold_ingot",model:"minecraft:gold_ingot",desc:"골드를 얻는다",color:"#E0B255"},\
k4:{k:4,name:"상점",item:"minecraft:emerald",model:"minecraft:emerald",desc:"아이템 · 회복 구매",color:"#6FCF8F"},\
k5:{k:5,name:"사파이어",item:"minecraft:diamond",model:"minecraft:diamond",desc:"사파이어 2개",color:"#5B9BF0"},\
k7:{k:7,name:"인챈트",item:"minecraft:enchanted_book",model:"minecraft:enchanted_book",desc:"아이템 강화 2~4번",color:"#B58BE8"},\
k8:{k:8,name:"나무뿌리",item:"minecraft:mangrove_roots",model:"minecraft:mangrove_roots",desc:"각인에 기적 (한 번뿐)",color:"#B08A5A"},\
k10:{k:10,name:"레벨업",item:"minecraft:experience_bottle",model:"minecraft:experience_bottle",desc:"경험의 샘 (레벨 업)",color:"#8FD46A"},\
k11:{k:11,name:"주사위",item:"minecraft:white_dye",model:"rlk:dice",desc:"주사위 2개 (리롤권)",color:"#F2F2F2"},\
k12:{k:12,name:"보유 칸",item:"minecraft:bundle",model:"minecraft:bundle",desc:"아이템 보유 칸 +2",color:"#4FC3C9"},\
k13:{k:13,name:"생명력",item:"minecraft:golden_apple",model:"minecraft:golden_apple",desc:"최대 체력 +10%",color:"#E06A8A"},\
k14:{k:14,name:"아이템",item:"minecraft:chest",model:"minecraft:chest",desc:"아이템 하나 고르기",color:"#FFE08A"},\
k15:{k:15,name:"중간보스",item:"minecraft:wither_skeleton_skull",model:"minecraft:wither_skeleton_skull",desc:"강적 처치 → 아이템 선택 2번",color:"#E0703A"}\
}
# 뽑기 가중치 (클수록 자주). 상점은 반드시 다른 노드와 함께, 나무뿌리는 한 판에 한 번(#mirUsed), 보유 칸은 3챕터부터 · 18칸 미만일 때만
# 중간보스(15)는 1챕터 첫 선택지에는 안 나오고, 뽑을 수 있는 중간보스(가중치 1 이상)가 등록되어 있을 때만 나옴
data modify storage rlk:room nw set value [{k:3,w:10},{k:4,w:8},{k:5,w:7},{k:7,w:8},{k:8,w:5},{k:10,w:9},{k:11,w:8},{k:12,w:3},{k:13,w:7},{k:14,w:8},{k:15,w:7}]
