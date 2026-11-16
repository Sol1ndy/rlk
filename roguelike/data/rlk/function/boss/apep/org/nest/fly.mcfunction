execute unless entity @e[tag=rlk_body,distance=..12] run return run function rlk:boss/apep/org/nest/blink_go
execute unless entity @e[tag=rlk_body,distance=..8] facing entity @e[tag=rlk_body,limit=1] feet run function rlk:mboss/mv/step_flat {spd:0.15}
execute if entity @e[tag=rlk_body,distance=..4] facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run function rlk:mboss/mv/step_flat {spd:0.15}
function rlk:boss/apep/org/nest/push_out
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
scoreboard players operation #apM mb = @s apT
scoreboard players operation #apM mb %= #apC14 mb
execute if score #apM mb matches 0 at @s run function rlk:boss/apep/fx/snd/o4_flap
scoreboard players remove @s apTok 1
execute if score @s apTok matches 1.. run return 0
# never while a 파괴 is within 6 b of the Heart or fusing, never during a 포식성 bite chain
function rlk:boss/apep/org/nest/flags
execute if score #apDNear mb matches 1 run return run scoreboard players set @s apTok 10
execute if score #apPChain mb matches 1 run return run scoreboard players set @s apTok 10
execute unless score #apPh mb matches 2 run return run scoreboard players set @s apTok 10
function rlk:boss/apep/org/nest/cast_go
