# 아이템 선택 공간 안 (@s = 플레이어, 매 틱): 핫바 0~2(무기·스킬·폭발)는 빈 아이템으로, 3~8 은 비어 있을 때만 빈 아이템으로
execute unless items entity @s hotbar.0 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:0}}] run item replace entity @s hotbar.0 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:0}}]
execute unless items entity @s hotbar.1 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:1}}] run item replace entity @s hotbar.1 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:1}}]
execute unless items entity @s hotbar.2 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:2}}] run item replace entity @s hotbar.2 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:2}}]
execute unless items entity @s hotbar.3 * run item replace entity @s hotbar.3 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:3}}]
execute if items entity @s hotbar.3 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] unless items entity @s hotbar.3 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:3}}] run item replace entity @s hotbar.3 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:3}}]
execute unless items entity @s hotbar.4 * run item replace entity @s hotbar.4 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:4}}]
execute if items entity @s hotbar.4 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] unless items entity @s hotbar.4 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:4}}] run item replace entity @s hotbar.4 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:4}}]
execute unless items entity @s hotbar.5 * run item replace entity @s hotbar.5 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:5}}]
execute if items entity @s hotbar.5 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] unless items entity @s hotbar.5 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:5}}] run item replace entity @s hotbar.5 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:5}}]
execute unless items entity @s hotbar.6 * run item replace entity @s hotbar.6 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:6}}]
execute if items entity @s hotbar.6 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] unless items entity @s hotbar.6 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:6}}] run item replace entity @s hotbar.6 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:6}}]
execute unless items entity @s hotbar.7 * run item replace entity @s hotbar.7 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:7}}]
execute if items entity @s hotbar.7 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] unless items entity @s hotbar.7 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:7}}] run item replace entity @s hotbar.7 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:7}}]
execute unless items entity @s hotbar.8 * run item replace entity @s hotbar.8 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:8}}]
execute if items entity @s hotbar.8 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] unless items entity @s hotbar.8 *[minecraft:custom_data~{rlk_ui:{role:"blank",s:8}}] run item replace entity @s hotbar.8 with minecraft:stick[minecraft:item_model="rlk:empty",minecraft:item_name={text:""},minecraft:tooltip_display={hide_tooltip:true},minecraft:max_stack_size=1,minecraft:custom_data={rlk_ui:{role:"blank",s:8}}]
# 버린 빈 아이템은 없앤다
execute as @e[type=minecraft:item,distance=..8] if items entity @s contents *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run kill @s

# 칸마다 한 개(겹치기 불가). 핫바 밖으로 옮긴 빈 아이템은 없앤다(인벤토리 · 커서)
execute if items entity @s inventory.0 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.0 with air
execute if items entity @s inventory.1 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.1 with air
execute if items entity @s inventory.2 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.2 with air
execute if items entity @s inventory.3 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.3 with air
execute if items entity @s inventory.4 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.4 with air
execute if items entity @s inventory.5 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.5 with air
execute if items entity @s inventory.6 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.6 with air
execute if items entity @s inventory.7 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.7 with air
execute if items entity @s inventory.8 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.8 with air
execute if items entity @s inventory.9 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.9 with air
execute if items entity @s inventory.10 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.10 with air
execute if items entity @s inventory.11 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.11 with air
execute if items entity @s inventory.12 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.12 with air
execute if items entity @s inventory.13 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.13 with air
execute if items entity @s inventory.14 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.14 with air
execute if items entity @s inventory.15 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.15 with air
execute if items entity @s inventory.16 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.16 with air
execute if items entity @s inventory.17 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.17 with air
execute if items entity @s inventory.18 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.18 with air
execute if items entity @s inventory.19 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.19 with air
execute if items entity @s inventory.20 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.20 with air
execute if items entity @s inventory.21 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.21 with air
execute if items entity @s inventory.22 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.22 with air
execute if items entity @s inventory.23 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.23 with air
execute if items entity @s inventory.24 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.24 with air
execute if items entity @s inventory.25 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.25 with air
execute if items entity @s inventory.26 *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s inventory.26 with air
execute if items entity @s player.cursor *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] run item replace entity @s player.cursor with air