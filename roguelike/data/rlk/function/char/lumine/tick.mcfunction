# 루미네 매 틱 (@s = 플레이어, at @s): 혹한의 별 / 투창 차례로 던지기 / 차가운 별빛 표시
execute as @e[tag=rlk_lstar,limit=1] run function rlk:char/lumine/star_tick
execute if score @s javQ matches 1.. run function rlk:char/lumine/jav_queue
# 예리한 얼음: 남은 시간(사이드바에 초로 표시) + 손 주변 냉기
execute if score @s lumP matches 1.. run function rlk:char/lumine/passive_tick
execute unless score @s lumP matches 1.. run scoreboard players reset 예리한얼음 stacks
execute if score @s starlight matches 1.. run scoreboard players operation 차가운별빛 stacks = @s starlight
execute if score @s starlight matches 1.. run scoreboard players display name 차가운별빛 stacks {text:"차가운 별빛",color:"#9FE8FF"}
execute unless score @s starlight matches 1.. run scoreboard players reset 차가운별빛 stacks
