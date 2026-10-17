# 중간보스 아이템 상자(oact 15, @s = 상자 오브젝트, at @s): 상자 하나 = 챕터 등급 아이템 선택 1번.
# pkMb +1 이라 이 묶음에는 캐릭터 카드가 나오지 않는다(lvup/roll). 누른 상자만 사라지고(kill_group) 바로 선택 화면으로
execute as @a[tag=player,limit=1] run scoreboard players add @s pkMb 1
execute as @a[tag=player,limit=1] run function rlk:lvup/add {n:1}
playsound minecraft:block.chest.open block @a[tag=player] ~ ~ ~ 0.9 1
playsound minecraft:block.amethyst_block.chime block @a[tag=player] ~ ~ ~ 1 1.2
particle minecraft:dust{color:[1.0f,0.84f,0.36f],scale:1.4f} ~ ~ ~ 0.35 0.35 0.35 0 18
particle minecraft:end_rod ~ ~0.2 ~ 0.15 0.15 0.15 0.1 12
function rlk:room/obj/kill_group
execute as @a[tag=player,limit=1] at @s unless score @s pkMode matches 1.. run function rlk:lvup/toggle
