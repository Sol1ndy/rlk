# 지도 아이템은 더 이상 주지 않는다(왼손 지도 · 3번 칸 버튼 제거). 남은 것만 치운다. 전체 지도 화면은 room/map_frame 이 액자에 직접 넣는다.
clear @s minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}]
clear @s *[minecraft:custom_data~{rlk_ui:{role:"map"}}]
