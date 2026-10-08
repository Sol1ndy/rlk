# 플레이어가 어떤 칸의 진입 범위에 들어섬 (@s = 칸 표식) → 그 구역이 '건설됨(아직 안 들어감)'이면 진입 처리
scoreboard players operation #zb tmp = @s zid
execute as @e[tag=rlk_zone,scores={zst=1}] if score @s zid = #zb tmp at @s run function rlk:room/zone_enter
