# 첫 구역의 '플레이어 반대쪽' 지점
$execute if score @s zkind matches 8 positioned $(x).0 201 $(z).0 run function rlk:room/obj/k_root
$execute if score @s zkind matches 10 run summon minecraft:marker $(x).0 201 $(z).0 {Tags:["rlk_room","rlk_xpspot"]}
