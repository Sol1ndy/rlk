scoreboard players add @s nfQ 1
execute if score @s nfQ matches 13 at @e[tag=rlk_nfq,limit=1] rotated as @e[tag=rlk_nfq,limit=1] run function rlk:char/nefer/burst_hit {a:112,e:67}
execute if score @s nfQ matches 14.. run kill @e[tag=rlk_nfq]
execute if score @s nfQ matches 14.. run scoreboard players set @s nfQ 0
