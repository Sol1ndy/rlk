# 스커크 매 틱 (@s = 플레이어, at 몸)
scoreboard players set #skMode tmp 0
execute if score @s skM matches 1.. run scoreboard players set #skMode tmp 1
execute if score @s skDepCd matches 1.. run scoreboard players remove @s skDepCd 1
execute if score #skRiftCd tmp matches 1.. run scoreboard players remove #skRiftCd tmp 1
execute if score @s skQ matches 1.. run function rlk:char/skirk/q_tick
execute if score @s skM matches 1.. run function rlk:char/skirk/mode_tick
execute if score @s skDash matches 1.. run function rlk:char/skirk/dash_tick
execute if score @s skBurst matches 1.. run function rlk:char/skirk/burst_tick
execute as @e[tag=rlk_rift] at @s run function rlk:char/skirk/rift_tick
execute if score @s skDep matches 1.. run scoreboard players operation 고갈 stacks = @s skDep
execute if score @s skDep matches 1.. run scoreboard players display name 고갈 stacks {text:"고갈 (강화 공격)",color:"#C9A6FF"}
execute unless score @s skDep matches 1.. run scoreboard players reset 고갈 stacks
