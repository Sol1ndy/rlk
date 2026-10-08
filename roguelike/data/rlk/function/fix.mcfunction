# 캐릭터 즉시 복구: 스탯/속성 기본값으로 재초기화 (@s = 플레이어)
execute as @s[type=minecraft:player] run scoreboard players set @s init 0
execute as @s[type=minecraft:player] run function rlk:player/init
tellraw @s {"text":"[로그라이크] 캐릭터를 복구했습니다.","color":"yellow"}
