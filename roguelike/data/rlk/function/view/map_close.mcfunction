# 새 화면과 구버전 관전 화면 모두 안전하게 복귀한다.
execute if entity @s[gamemode=spectator] run spectate
ride @s dismount
execute if entity @s[tag=rlk_mgS] run gamemode survival @s
execute if entity @s[tag=rlk_mgA] run gamemode adventure @s
execute if entity @s[tag=rlk_mgC] run gamemode creative @s
execute unless entity @s[tag=rlk_mgS] unless entity @s[tag=rlk_mgA] unless entity @s[tag=rlk_mgC] run gamemode adventure @s
execute if data storage rlk:map ret.x run function rlk:view/map_restore with storage rlk:map ret
execute unless data storage rlk:map ret.x at @e[tag=rlk_body,limit=1] run tp @s ~ ~2 ~
execute if data storage rlk:map ret{was_body:1b} run tag @s add rlk_body
kill @e[tag=rlk_mapreturn]
scoreboard players set @s vMap 0
scoreboard players set @s vMapH 8
scoreboard players set @s uiCd 8
scoreboard players set @s vSnk 1
scoreboard players set @s rcU 0
scoreboard players set @s rcT 0
execute if score #active room matches 1 if data storage rlk:room map_id run function rlk:room/map_give with storage rlk:room
tag @s remove rlk_mgS
tag @s remove rlk_mgA
tag @s remove rlk_mgC
data remove storage rlk:map ret
execute unless score #k204 snd matches 1 run function rlk:snd/f223
