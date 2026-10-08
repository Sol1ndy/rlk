# 캐릭터 정보 아이템 (@s = 플레이어): 인벤토리 0번 칸 = 플레이어 머리(캐릭터 설명), 1번 칸 = 종이 「고유 특성」, 2번 칸 = 종이(추가 설명 info.extra) — 있는 캐릭터만
clear @s *[minecraft:custom_data~{rlk_char:1b}]
function rlk:char/place_info2 with storage rlk:chars cur.info
execute if data storage rlk:chars cur.info.passive[0] run function rlk:char/place_pas with storage rlk:chars cur.info
execute if data storage rlk:chars cur.info.extra.lore[0] run function rlk:char/place_ext
