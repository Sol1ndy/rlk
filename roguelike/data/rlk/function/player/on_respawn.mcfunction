# 부활 직후 (@s = 플레이어): 체력 완충 + 원소 상태 정리
scoreboard players set @s dead 0
execute if score @s pkMode matches 1.. run function rlk:lvup/cleanup
# 부활 직후 바닐라 체력이 덜 차 있을 수 있으니 다시 채움
attribute @s minecraft:max_health base set 1024
effect give @s minecraft:instant_health 1 20 true
scoreboard players operation @s curHealth = @s maxHealth
function rlk:element/clear
scoreboard players set @s shieldHP 0
function rlk:player/hook_respawn
function rlk:view/sync
function rlk:view/input_stale
