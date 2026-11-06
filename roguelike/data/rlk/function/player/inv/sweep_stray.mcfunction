# 핫바 3~8번(빈칸)에 옮겨 놓은 특수아이템, 핫바 · 왼손에 옮겨 놓은 잠긴 칸 방벽 · 각인 칸 아이템, 커서에 든 방벽을 없앤다 (@s = 플레이어)
# 둘째·셋째 줄(inventory.9~26)은 place_items 가 칸마다 맞춰 놓으므로 따로 청소하지 않는다. 각인 칸 아이템이 줄면 engravings/tick 이 다시 만든다
execute if items entity @s hotbar.3 *[minecraft:custom_data~{rlk:{}}] run item replace entity @s hotbar.3 with air
execute if items entity @s hotbar.4 *[minecraft:custom_data~{rlk:{}}] run item replace entity @s hotbar.4 with air
execute if items entity @s hotbar.5 *[minecraft:custom_data~{rlk:{}}] run item replace entity @s hotbar.5 with air
execute if items entity @s hotbar.6 *[minecraft:custom_data~{rlk:{}}] run item replace entity @s hotbar.6 with air
execute if items entity @s hotbar.7 *[minecraft:custom_data~{rlk:{}}] run item replace entity @s hotbar.7 with air
execute if items entity @s hotbar.8 *[minecraft:custom_data~{rlk:{}}] run item replace entity @s hotbar.8 with air
execute if items entity @s hotbar.* *[minecraft:custom_data~{rlk_lock:1b}] run function rlk:player/inv/sweep_hotbar
execute if items entity @s hotbar.* *[minecraft:custom_data~{rlk_engi:1b}] run function rlk:player/inv/sweep_hotbar
execute if items entity @s player.cursor *[minecraft:custom_data~{rlk_lock:1b}] run item replace entity @s player.cursor with air
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_lock:1b}] run item replace entity @s weapon.offhand with air
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_engi:1b}] run item replace entity @s weapon.offhand with air
