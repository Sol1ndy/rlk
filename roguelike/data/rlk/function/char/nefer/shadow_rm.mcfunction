# 그림자 치우기: 죽는 모습이 보이지 않게, 아주 먼 곳(항상 불러 둔 청크)으로 보내 화면에서 먼저 사라지게 한 뒤 5틱 뒤에 없앤다
execute as @e[tag=rlk_nfsh] run data merge entity @s {Glowing:0b}
effect give @e[tag=rlk_nfsh] minecraft:invisibility 2 0 true
tp @e[tag=rlk_nfsh] 1000008 100 1000008
scoreboard players set @e[tag=rlk_nfsh] life 5
tag @e[tag=rlk_nfsh] add rlk_nfsh_dead
tag @e[tag=rlk_nfsh_dead] remove rlk_nfsh
