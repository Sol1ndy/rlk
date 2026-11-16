# 캐릭터 정보 아이템 (@s = 플레이어): 인벤토리 0번 칸 = 플레이어 머리(캐릭터 설명), 1번 칸 = 종이 「고유 특성」
# (추가 설명 info.extra 가 있는 캐릭터는 같은 종이 아래쪽에 붙인다. 2번 칸은 인벤토리 상세 버튼)
clear @s *[minecraft:custom_data~{rlk_char:1b}]
function rlk:char/place_info2 with storage rlk:chars cur.info
data modify storage rlk:chars pas set value {passive:[]}
data modify storage rlk:chars pas.color set from storage rlk:chars cur.info.color
execute if data storage rlk:chars cur.info.passive[0] run data modify storage rlk:chars pas.passive set from storage rlk:chars cur.info.passive
execute if data storage rlk:chars cur.info.extra.lore[0] run function rlk:char/place_ext
execute if data storage rlk:chars pas.passive[0] run function rlk:char/place_pas with storage rlk:chars pas
