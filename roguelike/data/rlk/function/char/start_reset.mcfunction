# @s = 플레이어. 지금 캐릭터가 시작 캐릭터가 아니면 바꾼다
data modify storage rlk:chars sc.id set from storage rlk:config start_char
function rlk:char/start_reset2 with storage rlk:chars sc
