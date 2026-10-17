# 구역에 처음 들어옴 (@s = 구역 표식, at @s). 이때 비로소 적/보상이 나타난다
scoreboard players set @s zst 2
function rlk:room/cells_kill
function rlk:room/wave_start
execute if score @s zkind matches 1 run return run function rlk:room/combat_start
execute if score @s zkind matches 9 run return run function rlk:room/combat_start
scoreboard players set @s zst 3
execute if score @s zkind matches 2 run function rlk:room/end_setup
execute if score @s zkind matches 3 run function rlk:room/obj/k_money
execute if score @s zkind matches 4 run function rlk:room/obj/k_shop
execute if score @s zkind matches 5 run function rlk:room/obj/k_sapphire
execute if score @s zkind matches 6 run function rlk:room/obj/k_reforge
execute if score @s zkind matches 7 run function rlk:room/obj/k_enchant
# 노드 구역(중간 구역): 8 나무뿌리, 10 레벨업(경험의 샘), 11 주사위, 12 보유 칸, 13 생명력, 14 아이템, 15 중간보스
execute if score @s zkind matches 8 run function rlk:room/obj/k_root
execute if score @s zkind matches 10 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_xpspot"]}
execute if score @s zkind matches 11 run function rlk:room/obj/k_dice
execute if score @s zkind matches 12 run function rlk:room/obj/k_slot
execute if score @s zkind matches 13 run function rlk:room/obj/k_hp
execute if score @s zkind matches 14 run function rlk:room/obj/k_item
# 15 중간보스: 문 오브젝트(누르면 전투 → 원형 경기장)
execute if score @s zkind matches 15 run function rlk:room/obj/k_mboss
execute unless score #k10 snd matches 1 run function rlk:snd/f10
