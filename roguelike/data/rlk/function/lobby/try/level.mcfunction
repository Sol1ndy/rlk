# 레벨 바꾸기 (@s = 플레이어): 1 → 20 → 40 → 60 → 80 → 100 → 처음
scoreboard players set #t lob 1
execute if score @s level matches 1..19 run scoreboard players set #t lob 20
execute if score @s level matches 20..39 run scoreboard players set #t lob 40
execute if score @s level matches 40..59 run scoreboard players set #t lob 60
execute if score @s level matches 60..79 run scoreboard players set #t lob 80
execute if score @s level matches 80..99 run scoreboard players set #t lob 100
scoreboard players operation @s level = #t lob
scoreboard players set @s xp 0
function rlk:player/level/apply
function rlk:items/equip_scan
scoreboard players operation @s curHealth = @s maxHealth
function rlk:lobby/try/labels
