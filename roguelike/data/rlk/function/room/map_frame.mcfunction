# 전체 지도 화면의 액자에 이번 던전 지도를 넣는다 (map_open, in overworld). 손에는 주지 않는다.
$item replace entity @e[tag=rlk_mapframe,limit=1] contents with minecraft:filled_map[minecraft:map_id=$(map_id),minecraft:custom_data={rlk_map:1b,v:3b},minecraft:item_name={text:"던전 지도",color:"gold",italic:false}]
