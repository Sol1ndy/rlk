# @s = 회수하려는 플레이어. 가진 아이템 8개 이하일 때만. 캐릭터 아이템이면 보유 칸과 상관없이 교체
function rlk:ditem/retrieve_getid with storage rlk:dtmp
function rlk:ditem/retrieve_ischar with storage rlk:dtmp
execute if score #isCh tmp matches 1 run return run function rlk:ditem/retrieve_char
execute store result score #cnt tmp run data get storage rlk:pinv order
execute if score #cnt tmp matches ..8 run function rlk:ditem/retrieve_ok
execute unless score #cnt tmp matches ..8 run function rlk:ditem/retrieve_full
