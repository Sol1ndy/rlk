# 가진 아이템 모두 버리기(캐릭터 · 레벨은 그대로) (@s = 플레이어): 초기화한 뒤 캐릭터 · 레벨을 되돌림
data modify storage rlk:lobby keep.id set from storage rlk:chars cur.id
scoreboard players operation #lvKeep lob = @s level
function rlk:player/reset_one
function rlk:char/switch with storage rlk:lobby keep
scoreboard players operation @s level = #lvKeep lob
function rlk:player/level/apply
function rlk:items/equip_scan
scoreboard players operation @s curHealth = @s maxHealth
title @s actionbar {text:"아이템을 모두 버렸습니다",color:"gray"}
scoreboard players set @s hudHold 30
