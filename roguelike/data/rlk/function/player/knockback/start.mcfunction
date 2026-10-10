# @s = 피해를 받은 실제 플레이어. 피격 확인 후 한 번만 호출한다.
execute if score @s dead matches 1 run return 0
execute if score @s curHealth matches ..0 run return 0
execute if score @s rnDie matches 1.. run return 0
execute if score @s pkMode matches 1.. run return 0
execute if score @s vMap matches 1 run return 0
execute if score @s dashInvT matches 1.. run return 0
execute if score @s dashMoveT matches 1.. run return 0
# 여러 번 맞아도 이동량을 무한 누적하지 않고 마지막 타격 방향으로 갱신한다.
kill @e[tag=rlk_plkb]
execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ ~ ~ {Tags:["rlk_plkb"]}
execute at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_plkb_source,limit=1] run tp @e[tag=rlk_plkb,limit=1] ~ ~ ~ ~ 0
scoreboard players operation @e[tag=rlk_plkb,limit=1] pkbT = #cmKB tmp
# 검격의 전진 예약은 밀려나는 동안 종료. 대쉬 값은 재사용하지 않는다.
scoreboard players set @s stepT 0
execute if entity @e[tag=rlk_av,limit=1] run function rlk:view/stop_h
execute as @e[tag=rlk_plkb,limit=1] run function rlk:player/knockback/tick
