# 실제 왼손 지도 + 클릭용 4번 칸. 종이 버튼에는 map_id를 넣지 않아 손 지도가 중복 렌더링되지 않는다.
clear @s minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}]
clear @s *[minecraft:custom_data~{rlk_ui:{role:"map"}}]
$item replace entity @s weapon.offhand with minecraft:filled_map[minecraft:map_id=$(map_id),minecraft:custom_data={rlk_map:1b,v:3b},minecraft:item_name={text:"던전 지도",color:"gold",italic:false}]
item replace entity @s hotbar.3 with minecraft:paper[minecraft:item_model="rlk:map_button",minecraft:custom_data={rlk_map_button:1b,v:3b,rlk_ui:{role:"map"}},minecraft:item_name={text:"던전 지도 · 좌/우클릭",color:"gold",italic:false},minecraft:max_stack_size=1,minecraft:consumable={consume_seconds:1000000f,animation:"none",sound:"minecraft:intentionally_empty",has_consume_particles:false}]
