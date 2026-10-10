# 앞(0.9칸) 발·머리 높이 막힘 → #bF #bH
scoreboard players set #bF tmp 0
scoreboard players set #bH tmp 0
execute at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^0.4 ^0.9 unless block ~ ~ ~ #rlk:cm_pass run scoreboard players set #bF tmp 1
execute at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^1.5 ^0.9 unless block ~ ~ ~ #rlk:cm_pass run scoreboard players set #bH tmp 1
execute at @s rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 positioned ^ ^2.2 ^0.9 unless block ~ ~ ~ #rlk:cm_pass run scoreboard players set #bH tmp 1
