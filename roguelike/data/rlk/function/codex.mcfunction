# 아이템 도감 열기/닫기 (@s = 플레이어). 사용: /function rlk:codex
execute unless entity @s[type=minecraft:player] run return fail
execute at @s run function rlk:codex/open
