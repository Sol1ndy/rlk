# 스탯 표시 아이템(gold ingot) - 인벤토리 우측 상단(inventory.8)에 고정
# 표시 값이 바뀌었거나 아이템이 제자리에 없을 때만 재생성 (매 틱 재생성 금지: 인벤 dirty 유발 방지)
scoreboard players set #uh tmp 0
scoreboard players operation #uh tmp += @s level
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s xp
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s curHealth
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s maxHealth
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s atk
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s base_atk
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s def
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s base_def
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s elemMastery
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s moveSpeed
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s atkSpeed
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s critChance
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s critDamage
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s gold
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s sapphire
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s energyRecharge
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s physBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s pyroBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s hydroBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s electroBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s cryoBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s geoBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s anemoBonus
scoreboard players operation #uh tmp *= #31 tmp
scoreboard players operation #uh tmp += @s dendroBonus

# 값 동일 + 아이템 제자리 → 스킵
execute if score #uh tmp = @s uiHash if items entity @s inventory.8 minecraft:gold_ingot[minecraft:custom_data~{rlk_stat:1b}] run return 0
scoreboard players operation @s uiHash = #uh tmp

# 어느 슬롯에 있든 스탯 아이템 모두 제거 (커서/다른 칸으로 옮겨도 회수)
clear @s minecraft:gold_ingot[minecraft:custom_data~{rlk_stat:1b}]

# 표시할 값 저장 (추가 수치 = 최종 − 기초)
execute store result storage rlk:item lv int 1 run scoreboard players get @s level
execute store result storage rlk:item xp int 1 run scoreboard players get @s xp
execute store result storage rlk:item xn int 1 run scoreboard players get @s xpNeed
execute store result storage rlk:item ch int 1 run scoreboard players get @s curHealth
execute store result storage rlk:item mh int 1 run scoreboard players get @s maxHealth
execute store result storage rlk:item hb int 1 run scoreboard players get @s base_maxHealth
scoreboard players operation #ub tmp = @s maxHealth
scoreboard players operation #ub tmp -= @s base_maxHealth
execute store result storage rlk:item hx int 1 run scoreboard players get #ub tmp
execute store result storage rlk:item pa int 1 run scoreboard players get @s atk
execute store result storage rlk:item ab int 1 run scoreboard players get @s base_atk
scoreboard players operation #ub tmp = @s atk
scoreboard players operation #ub tmp -= @s base_atk
execute store result storage rlk:item ax int 1 run scoreboard players get #ub tmp
execute store result storage rlk:item df int 1 run scoreboard players get @s def
execute store result storage rlk:item db int 1 run scoreboard players get @s base_def
scoreboard players operation #ub tmp = @s def
scoreboard players operation #ub tmp -= @s base_def
execute store result storage rlk:item fx int 1 run scoreboard players get #ub tmp
execute store result storage rlk:item ma int 1 run scoreboard players get @s elemMastery
execute store result storage rlk:item mv int 1 run scoreboard players get @s moveSpeed
execute store result storage rlk:item sp int 1 run scoreboard players get @s atkSpeed
execute store result storage rlk:item cc int 1 run scoreboard players get @s critChance
execute store result storage rlk:item cd int 1 run scoreboard players get @s critDamage
execute store result storage rlk:item gd int 1 run scoreboard players get @s gold
execute store result storage rlk:item sa int 1 run scoreboard players get @s sapphire
execute store result storage rlk:item er int 1 run scoreboard players get @s energyRecharge
execute store result storage rlk:item b0 int 1 run scoreboard players get @s physBonus
execute store result storage rlk:item b1 int 1 run scoreboard players get @s pyroBonus
execute store result storage rlk:item b2 int 1 run scoreboard players get @s hydroBonus
execute store result storage rlk:item b3 int 1 run scoreboard players get @s electroBonus
execute store result storage rlk:item b4 int 1 run scoreboard players get @s cryoBonus
execute store result storage rlk:item b5 int 1 run scoreboard players get @s geoBonus
execute store result storage rlk:item b6 int 1 run scoreboard players get @s anemoBonus
execute store result storage rlk:item b7 int 1 run scoreboard players get @s dendroBonus

function rlk:player/update_item_macro with storage rlk:item
