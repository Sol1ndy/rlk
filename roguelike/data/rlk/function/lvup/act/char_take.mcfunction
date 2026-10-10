# 캐릭터 교체 (@s = 플레이어): 지금 캐릭터의 아이템을 "돌아갈 때 떨굴 목록"에 넣고 새 캐릭터로 바꾼다
data modify storage rlk:lvpick dropq append from storage rlk:chars cur.itemId
function rlk:char/switch with storage rlk:lvpick ch
execute unless score #k2 snd matches 1 run function rlk:snd/f415
execute unless score #k73 snd matches 1 run function rlk:snd/f78
function rlk:lvup/act/resolve
