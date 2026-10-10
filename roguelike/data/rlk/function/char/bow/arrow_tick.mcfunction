# @s = 날아가는 화살, at @s (매 틱)
scoreboard players add @s life 1
execute if score @s life > @s aLife run return run function rlk:char/bow/arrow_end
# 염초 화살: 가까운 적을 쫓는다
execute if score @s aKind matches 4 positioned ^ ^ ^2 if entity @e[tag=rlk_mob,distance=..24] run function rlk:char/bow/arrow_home
# 로노바 평타(7): 조준해서 선택한 적만 추적. 허공·벽을 쐈거나 대상이 사라지면 직진한다.
execute if score @s aKind matches 7 if score @s life matches 2.. if score @s rnTg matches 1.. run function rlk:char/ronova/na_home
# 잔향(8): 기존의 근처 적 추적을 유지한다.
execute if score @s aKind matches 8 positioned ^ ^ ^2 if entity @e[tag=rlk_mob,distance=..16] run function rlk:char/bow/arrow_home
scoreboard players set #jend tmp 0
scoreboard players operation #as tmp = @s aSub
execute at @s run function rlk:char/bow/arrow_step
execute if score #jend tmp matches 0 at @s run function rlk:char/bow/arrow_trail
