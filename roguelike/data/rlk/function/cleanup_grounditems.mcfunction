# 버려진 UI/시스템 아이템 제거 (다음 틱에 핫바/인벤 잠금이 제자리로 복귀시킴)
# 바닥에 아이템이 있을 때만 호출됨(메인 tick에서 게이팅)
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_ui:{}}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_stat:1b}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_eng:1b}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_engi:1b}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_invd:1b}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_lock:1b}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk:{}}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_map:1b}}}}]
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{rlk_char:1b}}}}]
