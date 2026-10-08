# 왼손에 던전 지도 (@s = 플레이어). 다른 칸으로 옮긴 사본은 지움
clear @s minecraft:filled_map[minecraft:custom_data~{rlk_map:1b}]
$item replace entity @s weapon.offhand with minecraft:filled_map[minecraft:map_id=$(map_id),minecraft:custom_data={rlk_map:1b},minecraft:item_name={text:"던전 지도",color:"gold",italic:false}]
