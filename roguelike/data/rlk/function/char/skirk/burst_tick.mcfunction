# 멸 진행 (@s = 플레이어): 1·3·5·7·9틱에 빠른 참격 5번, 잠시 뒤 13틱에 마지막 참격
execute if score @s skBurst matches 1 at @e[tag=rlk_skb,limit=1] run function rlk:char/skirk/slash {coef:220}
execute if score @s skBurst matches 3 at @e[tag=rlk_skb,limit=1] run function rlk:char/skirk/slash {coef:220}
execute if score @s skBurst matches 5 at @e[tag=rlk_skb,limit=1] run function rlk:char/skirk/slash {coef:220}
execute if score @s skBurst matches 7 at @e[tag=rlk_skb,limit=1] run function rlk:char/skirk/slash {coef:220}
execute if score @s skBurst matches 9 at @e[tag=rlk_skb,limit=1] run function rlk:char/skirk/slash {coef:220}
execute if score @s skBurst matches 13 at @e[tag=rlk_skb,limit=1] run function rlk:char/skirk/slash {coef:370}
scoreboard players add @s skBurst 1
execute if score @s skBurst matches 14.. run kill @e[tag=rlk_skb]
execute if score @s skBurst matches 14.. run scoreboard players set @s skBurst 0
