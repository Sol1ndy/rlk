# 핫바 잠금 (@s = 플레이어, at @s)
# F(양손 바꾸기)로 UI 아이템이 오프핸드에 오면 회수 + 대쉬
# 무기를 든 채 웅크리고 F(Shift+F) = 레벨 업 아이템 선택 공간으로 이동/복귀
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"attack"}}] if score @s sneakT matches 1.. run function rlk:lvup/toggle
# 아이템 선택 공간 안(핫바 = 빈 아이템)에서도 Shift+F 로 돌아온다
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{role:"blank"}}] if score @s sneakT matches 1.. run function rlk:lvup/toggle
# 웅크리지 않고 F = 대쉬 (무기·스킬·폭발 아이템을 들고 있을 때). 활을 든 채로는 조준 시작/취소
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{}}] unless score @s sneakT matches 1.. run function rlk:player/f_key
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{}}] run item replace entity @s weapon.offhand with air
# 개발자 모드가 아니면 고정 UI 유지
execute unless score @s devMode matches 1 run function rlk:player/hotbar/place
