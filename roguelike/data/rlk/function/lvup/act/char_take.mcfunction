# 캐릭터 교체 (@s = 플레이어): 지금 캐릭터의 아이템을 "돌아갈 때 떨굴 목록"에 넣고 새 캐릭터로 바꾼다
data modify storage rlk:lvpick dropq append from storage rlk:chars cur.itemId
function rlk:char/switch with storage rlk:lvpick ch
playsound minecraft:entity.player.levelup master @s ~ ~ ~ 0.5 1.6
playsound minecraft:block.beacon.power_select master @s ~ ~ ~ 0.5 1.4
function rlk:lvup/act/resolve
