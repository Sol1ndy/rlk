# @s = follow hazard. Horizontal chase (pitch 0) at data.fv blocks per tick; snaps when closer than one step.
execute unless entity @e[tag=rlk_body,limit=1] run return 0
execute store result score #rdT rd run data get entity @s data.fv 1000
scoreboard players operation #rdPX rd = #rdBX rd
scoreboard players operation #rdPZ rd = #rdBZ rd
scoreboard players operation #rdPX rd -= @s rdHOX
scoreboard players operation #rdPZ rd -= @s rdHOZ
scoreboard players operation #rdR2 rd = #rdPX rd
scoreboard players operation #rdR2 rd *= #rdPX rd
scoreboard players operation #rdC rd = #rdPZ rd
scoreboard players operation #rdC rd *= #rdPZ rd
scoreboard players operation #rdR2 rd += #rdC rd
scoreboard players operation #rdC rd = #rdT rd
scoreboard players operation #rdC rd *= #rdT rd
execute if score #rdR2 rd <= #rdC rd at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/hazard/k/follow_snap
execute if score #rdR2 rd > #rdC rd facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/raiden/hazard/k/follow_step with entity @s data
scoreboard players operation #rdOwner rd = @s rdHId
execute at @s as @e[tag=rlk_rd_hvis,distance=..3] if score @s rdVId = #rdOwner rd run tp @s ~ ~ ~
# the cached origin follows the marker
execute store result score @s rdHOX run data get entity @s Pos[0] 1000
execute store result score @s rdHOY run data get entity @s Pos[1] 1000
execute store result score @s rdHOZ run data get entity @s Pos[2] 1000
