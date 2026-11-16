# 인벤토리 상세의 설명 창 위치 (@s = 플레이어, 매 틱). 칸은 9칸씩 두 줄: 열 = pkHI mod 9, 0~4 = 왼쪽 절반
scoreboard players set #9 tmp 9
scoreboard players operation #col tmp = @s pkHI
scoreboard players operation #col tmp %= #9 tmp
execute if score @s pkHK matches 2 if score #col tmp matches ..4 at @s anchored eyes positioned ^-1.6 ^ ^3 run tp @e[tag=rlk_pk_tip] ~ ~ ~
execute if score #col tmp matches ..4 at @s anchored eyes positioned ^1.6 ^ ^3 run tp @e[tag=rlk_pk_tip2] ~ ~ ~
execute if score #col tmp matches 5.. at @s anchored eyes positioned ^-1.6 ^ ^3 run tp @e[tag=rlk_pk_tip2] ~ ~ ~
