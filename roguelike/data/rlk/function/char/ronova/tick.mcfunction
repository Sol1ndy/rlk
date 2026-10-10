# 로노바 매 틱 (@s = 플레이어, at 몸)
execute if score @s rnFcd matches 1.. run scoreboard players remove @s rnFcd 1
execute if score @s rnEcd matches 1.. run scoreboard players remove @s rnEcd 1
# 불사의 저주로 쓰러져 있는 중
execute if score @s rnDie matches 1.. run function rlk:char/ronova/die_tick
execute if score @s rnQ matches 1.. run function rlk:char/ronova/q_tick
# 잔향 수 · 표시
scoreboard players set @s rnEn 0
execute if score @s rnE1 matches 1.. run scoreboard players add @s rnEn 1
execute if score @s rnE2 matches 1.. run scoreboard players add @s rnEn 1
execute if score @s rnE3 matches 1.. run scoreboard players add @s rnEn 1
function rlk:char/ronova/ec_tick
# 떠 있는 법구(숄더뷰)
function rlk:char/ronova/cat_tick
# 사이드바: 잔향 · 불사의 저주
execute if score @s rnEn matches 1.. run scoreboard players operation 잔향 stacks = @s rnEn
execute if score @s rnEn matches 1.. run scoreboard players display name 잔향 stacks {text:"잔향",color:"#E0365F"}
execute unless score @s rnEn matches 1.. run scoreboard players reset 잔향 stacks
execute unless score @s rnRev matches 1.. run scoreboard players set 불사의저주 stacks 1
execute unless score @s rnRev matches 1.. run scoreboard players display name 불사의저주 stacks {text:"불사의 저주 (대기)",color:"gray"}
execute if score @s rnRev matches 1.. run scoreboard players reset 불사의저주 stacks
