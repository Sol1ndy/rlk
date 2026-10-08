# 조준선으로 고르는 UI(상점·드롭 아이템·방 오브젝트)의 레이 길이(단계 수). 숄더뷰에서는 카메라가 뒤에 있으니 그만큼 길게
scoreboard players set #rObj view 15
scoreboard players set #rDit view 13
scoreboard players set #rDitB view 15
scoreboard players set #rShop view 16
scoreboard players set #rShopB view 15
execute if score #on view matches 1 run scoreboard players set #rObj view 27
execute if score #on view matches 1 run scoreboard players set #rDit view 21
execute if score #on view matches 1 run scoreboard players set #rDitB view 23
execute if score #on view matches 1 run scoreboard players set #rShop view 28
execute if score #on view matches 1 run scoreboard players set #rShopB view 27
