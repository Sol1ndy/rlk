# @s = 날아가는 화살, at @s (매 틱)
scoreboard players add @s life 1
execute if score @s life > @s aLife run return run function rlk:char/bow/arrow_end
# 염초 화살: 가까운 적을 쫓는다
execute if score @s aKind matches 4 positioned ^ ^ ^2 if entity @e[tag=rlk_mob,distance=..24] run function rlk:char/bow/arrow_home
# 로노바의 구체(7) · 잔향(8): 16칸 안의 적을 쫓는다
execute if score @s aKind matches 7..8 positioned ^ ^ ^2 if entity @e[tag=rlk_mob,distance=..16] run function rlk:char/bow/arrow_home
scoreboard players set #jend tmp 0
scoreboard players operation #as tmp = @s aSub
execute at @s run function rlk:char/bow/arrow_step
execute if score #jend tmp matches 0 at @s run function rlk:char/bow/arrow_trail
