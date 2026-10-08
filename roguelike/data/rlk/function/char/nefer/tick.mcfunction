# 네페르 매 틱 (@s = 플레이어, at 몸)
# 스킬 충전(최대 2). 충전이 하나도 없을 때만 스킬 칸에 남은 시간
execute unless score @s nfC matches 0.. run scoreboard players set @s nfC 2
execute unless score @s nfCdE matches 1.. run scoreboard players operation @s nfCdE = #nfCd tmp
execute if score @s nfC matches ..1 run scoreboard players add @s nfCT 1
execute if score @s nfC matches ..1 if score @s nfCT >= @s nfCdE run function rlk:char/nefer/charge
scoreboard players set @s skillCd 0
execute if score @s nfC matches 0 run scoreboard players operation @s skillCd = @s nfCdE
execute if score @s nfC matches 0 run scoreboard players operation @s skillCd -= @s nfCT
execute if score @s nfFcd matches 1.. run scoreboard players remove @s nfFcd 1
# 그림자 춤 · 환영극 · 원소폭발 · 기만의 장막 · 기만의 핵 시간
execute if score @s nfSD matches 1.. run scoreboard players remove @s nfSD 1
execute if score @s nfPT matches 1.. run function rlk:char/nefer/ph_tick
execute if score @s nfQ matches 1.. run function rlk:char/nefer/q_tick
execute if score @s nfVeilT matches 1.. run scoreboard players remove @s nfVeilT 1
execute if score @s nfVeilT matches 0 run scoreboard players set @s nfVeil 0
execute if score #nfDecT tmp matches 1.. run scoreboard players remove #nfDecT tmp 1
# 풀 이슬
execute if score @s nfDewW matches 1.. run function rlk:char/nefer/dew_tick
function rlk:char/nefer/dw_tick
function rlk:char/nefer/cat_tick
execute if score @s nfSD matches 1.. run particle minecraft:dust{color:[0.3,0.65,0.2],scale:0.8} ~ ~0.2 ~ 0.3 0.05 0.3 0 1
# 사이드바
execute if score @s nfDew matches 1.. run scoreboard players operation 풀이슬 stacks = @s nfDew
execute if score @s nfDew matches 1.. run scoreboard players display name 풀이슬 stacks {text:"풀 이슬",color:"#E9FFD6"}
execute unless score @s nfDew matches 1.. run scoreboard players reset 풀이슬 stacks
execute if score @s nfSD matches 1.. run scoreboard players operation 그림자춤 stacks = @s nfSD
execute if score @s nfSD matches 1.. run scoreboard players operation 그림자춤 stacks /= #st20 tmp
execute if score @s nfSD matches 1.. run scoreboard players add 그림자춤 stacks 1
execute if score @s nfSD matches 1.. run scoreboard players display name 그림자춤 stacks {text:"그림자 춤 (초)",color:"#7BD94A"}
execute unless score @s nfSD matches 1.. run scoreboard players reset 그림자춤 stacks
execute if score @s nfVeil matches 1.. run scoreboard players operation 기만의장막 stacks = @s nfVeil
execute if score @s nfVeil matches 1.. run scoreboard players display name 기만의장막 stacks {text:"기만의 장막",color:"#C9E8A0"}
execute unless score @s nfVeil matches 1.. run scoreboard players reset 기만의장막 stacks
