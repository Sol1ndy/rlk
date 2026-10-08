# 플레이어가 엔티티에게 맞은 순간 (@s = 플레이어, 발전과제 보상). 때린 몹의 원소 태그를 기록 → 다음 틱 player/take_damage 가 사용
# 몹 원소 태그: el_fire el_water el_thunder el_ice el_rock el_wind el_grass  (없으면 물리)
advancement revoke @s only rlk:element_hurt
scoreboard players set #e tmp 0
execute on attacker run function rlk:element/read_tag
scoreboard players operation @s hurtElem = #e tmp
# 때린 몹의 레벨 (공격력 보정용)
scoreboard players set #alv tmp 0
execute on attacker run scoreboard players operation #alv tmp = @s mlv
scoreboard players operation @s hurtLv = #alv tmp
