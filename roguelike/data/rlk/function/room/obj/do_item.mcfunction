# 아이템 구역: 아이템 선택 기회 1번 + 바로 선택 화면으로 (레벨 업 선택 화면과 같음, Shift+F 대신 클릭으로 들어감)
execute as @a[tag=player,limit=1] run function rlk:lvup/add {n:1}
execute unless score #k15 snd matches 1 run function rlk:snd/f15
function rlk:room/obj/kill_group
execute as @a[tag=player,limit=1] at @s unless score @s pkMode matches 1.. run function rlk:lvup/toggle
