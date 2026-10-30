# 중력의 물결 (@s = 플레이어, 위치 = 몸, #cgRipT > 0 인 동안 매 틱)
scoreboard players operation #t1 itv = #cgRipT itv
scoreboard players operation #t1 itv %= #st4 tmp
execute if score #t1 itv matches 0 run function rlk:items/proc/cg_rip_fx_pick
scoreboard players operation #t1 itv = #cgRipT itv
scoreboard players operation #t1 itv %= #cgRipInt tmp
execute if score #t1 itv matches 1 if entity @e[tag=rlk_mob,distance=..4,limit=1] run function rlk:items/proc/cg_rip_hit
# 사이드바: 중력
execute if score #cgG itv matches 1.. run scoreboard players operation 중력 stacks = #cgG itv
execute if score #cgG itv matches 1.. run scoreboard players display name 중력 stacks {text:"중력",color:"#C9D6FF"}
execute unless score #cgG itv matches 1.. run scoreboard players reset 중력 stacks
