# 경험치 획득 (@s = 플레이어, 입력: #xpAdd tmp). 넘치는 경험치는 다음 레벨로 이월
scoreboard players operation @s xp += #xpAdd tmp
execute if score @s xp >= @s xpNeed run function rlk:player/level/up
