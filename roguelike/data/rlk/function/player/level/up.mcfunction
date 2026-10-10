# 레벨 업 (@s = 플레이어)
scoreboard players operation @s xp -= @s xpNeed
scoreboard players add @s level 1
function rlk:items/stat_light
tellraw @s [{"text":"[레벨 업] ","color":"#8FD46A","bold":true},{"text":"Lv.","color":"white","bold":false},{"score":{"name":"@s","objective":"level"},"color":"white","bold":false},{"text":"  체력 +","color":"gray","bold":false},{"score":{"name":"#lvHpUp","objective":"tmp"},"color":"gray","bold":false},{"text":" · 공격력 +","color":"gray","bold":false},{"score":{"name":"#lvAtkUp","objective":"tmp"},"color":"gray","bold":false},{"text":" · 방어력 +","color":"gray","bold":false},{"score":{"name":"#lvDefUp","objective":"tmp"},"color":"gray","bold":false}]
execute at @s unless score #k208 snd matches 1 run function rlk:snd/f230
# 아이템 선택 기회 +1
scoreboard players add @s pkPending 1
tellraw @s [{"text":"[아이템 선택] ","color":"#FFE08A","bold":true},{"text":"웅크리기(Shift)","color":"white","bold":false},{"text":" 를 눌러 아이템을 고르세요. (1인칭에서는 무기를 들고 Shift + F · 전투 중에는 불가)","color":"gray","bold":false}]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:happy_villager ~ ~1 ~ 0.4 0.6 0.4 0 20
execute if score @s xp >= @s xpNeed run function rlk:player/level/up
