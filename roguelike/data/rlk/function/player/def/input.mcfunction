# 입력 앞 단계 (@s = 플레이어, at @s; rlk:tick 맨 앞, #now cb = 이번 틱 gametime). 이번 틱의 모든 피격보다 먼저 받아, 누른 틱이
# 어느 입력 경로로 와도 같은 창(누른 틱 = 0)이 되게 한다(연구 3.4).
# F: 무기 · 스킬 · 폭발 아이템이 왼손에 넘어옴(웅크리지 않음) = 패링(player/f_key). Shift+F 와 아이템 회수는 그대로 player/hotbar/tick
execute if items entity @s weapon.offhand *[minecraft:custom_data~{rlk_ui:{}}] unless score @s sneakT matches 1.. run function rlk:player/f_key
# 우클릭: 눈앞 입력 실드 · 몹 / 아바타 실드에 남은 우클릭을 지금 소비(combat/rclick_do → 무기면 닷지). 좌클릭은 그대로 틱 끝(combat/atkblock_manage)
execute as @e[type=minecraft:interaction,tag=atkBlock] if data entity @s interaction run function rlk:combat/input/poll_right
execute as @e[type=minecraft:interaction,tag=atkStrike] if data entity @s interaction run function rlk:combat/input/poll_right
execute as @e[type=minecraft:interaction,tag=rlk_mshield] if data entity @s interaction at @s run function rlk:combat/input/poll_right
# F5: 우클릭을 누르고 있음(아이템 사용 rlk:rc_use; 처음 틱과 4틱마다; 죽어 있는 동안은 버림). 지도 화면은 view/map_tick 이 받는다
execute unless score @s vMap matches 1 unless score @s dead matches 1 if score @s rcU matches 1 run function rlk:combat/rc_hold
execute unless score @s vMap matches 1 unless score @s rcU matches 1 run scoreboard players set @s rcT 0
execute unless score @s vMap matches 1 run scoreboard players set @s rcU 0
