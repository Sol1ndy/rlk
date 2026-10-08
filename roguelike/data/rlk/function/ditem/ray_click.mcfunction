# @s = 호버된 드롭 버튼, at @s. 좌클릭 처리 (일반 공격으로 이어지지 않게 플래그)
scoreboard players set #shopHandled tmp 1
function rlk:ditem/btn_click
tag @s remove rlk_dhover
