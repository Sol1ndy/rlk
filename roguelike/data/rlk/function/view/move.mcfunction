# 입력(WASD·점프·달리기) → 아바타 이동 (@s = 플레이어). 방향 기준 = 카메라가 보는 쪽
# 대쉬로 이동하는 동안은 건드리지 않음
scoreboard players set #inAct view 0
# 조준선을 봐야 하는 상태(#lk = 1)면 걷는 방향으로 몸을 돌리지 않는다
scoreboard players set #lk view 0
execute if score @s vAimT matches 1.. run scoreboard players set #lk view 1
execute if score @s buT matches 1.. run scoreboard players set #lk view 1
execute if score @s bowT matches 1.. run scoreboard players set #lk view 1
execute if score @s nvA matches 1.. run scoreboard players set #lk view 1
execute if score @s clAuto matches 1 run scoreboard players set #lk view 1
execute if score @s arSk matches 1.. run scoreboard players set #lk view 1
# 원소폭발의 이어지는 연타
execute if score @s javQ matches 1.. run scoreboard players set #lk view 1
execute if score @s skBurst matches 1.. run scoreboard players set #lk view 1
execute if score @s clBurst matches 1.. run scoreboard players set #lk view 1
execute if score @s rnQ matches 1.. run scoreboard players set #lk view 1
execute if score @s nfPT matches 1.. run scoreboard players set #lk view 1
execute if score @s nfQ matches 1.. run scoreboard players set #lk view 1
# 평타를 휘두르는 동안(swHold, player/swing/tick)은 걷는 방향으로 몸을 돌리지 않는다
execute if score @s swHold matches 1 run scoreboard players set #lk view 1
scoreboard players set #sprNow view 0
execute if score @s pmMoveLock matches 1 run return run function rlk:view/stop_h
execute if score @s dashMoveT matches 1.. run return 0
# 짧은 피격 이동 중에는 걷기 속도로 넉백을 덮어쓰지 않는다.
execute if entity @e[tag=rlk_plkb,limit=1] run return run function rlk:view/stop_h
# 원소폭발 시전 중 · 나비아 조준 중 · 로노바 쓰러짐 중에는 옆으로 움직이지 않는다(떨어지는 건 그대로)
execute if score @s nvA matches 1.. run return run function rlk:view/stop_h
execute if score @s buT matches 1.. run return run function rlk:view/stop_h
execute if score @s rnDie matches 1.. run return run function rlk:view/stop_h
# 부활 직후의 입력 상태는 죽기 전의 것일 수 있다 → 키를 하나라도 누르거나 떼서 상태가 달라질 때까지 무시
execute if score #inStale view matches 1 run function rlk:view/input_check
execute if score #inStale view matches 1 run return 0
scoreboard players set #f view 0
scoreboard players set #s view 0
execute if predicate rlk:in_f run scoreboard players add #f view 1
execute if predicate rlk:in_b run scoreboard players remove #f view 1
execute if predicate rlk:in_l run scoreboard players add #s view 1
execute if predicate rlk:in_r run scoreboard players remove #s view 1
# 점프: 땅에 서 있을 때만. 평타를 휘두르는 동안(swHold)은 뛰지 않는다. 평타 사이 간격에서 뛰면 다음 평타는 1타부터(player/swing/jump)
scoreboard players set #vJmp view 0
execute unless score @s swHold matches 1 if predicate rlk:in_jump as @e[tag=rlk_av,limit=1] if data entity @s {OnGround:1b} run scoreboard players set #vJmp view 1
execute if score #vJmp view matches 1 as @e[tag=rlk_av,limit=1] run data modify entity @s Motion[1] set value 0.42d
execute if score #vJmp view matches 1 run function rlk:player/swing/jump
# 입력이 없으면 그대로 둔다(마찰로 멈춤, 넉백도 그대로 받음)
execute if score #f view matches 0 if score #s view matches 0 run return 0
# 방향 표식을 아바타에서 1칸 떨어진 곳에: 표식 위치 - 아바타 위치 = 단위 방향 벡터
execute if score #f view matches 1 if score #s view matches 0 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~0 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches 1 if score #s view matches 1 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~-45 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches 0 if score #s view matches 1 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~-90 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches -1 if score #s view matches 1 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~-135 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches -1 if score #s view matches 0 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~180 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches -1 if score #s view matches -1 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~135 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches 0 if score #s view matches -1 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~90 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
execute if score #f view matches 1 if score #s view matches -1 at @e[tag=rlk_av,limit=1] rotated as @s rotated ~45 0 positioned ^ ^ ^1 run tp @e[tag=rlk_vmk,limit=1] ~ ~ ~
# 걷는 방향으로 몸 돌리기(조준선을 봐야 하는 상태가 아니면)
execute if score #lk view matches 0 run function rlk:view/turn
execute store result score #ax view run data get entity @e[tag=rlk_av,limit=1] Pos[0] 1000
execute store result score #az view run data get entity @e[tag=rlk_av,limit=1] Pos[2] 1000
execute store result score #mx view run data get entity @e[tag=rlk_vmk,limit=1] Pos[0] 1000
execute store result score #mz view run data get entity @e[tag=rlk_vmk,limit=1] Pos[2] 1000
scoreboard players operation #mx view -= #ax view
scoreboard players operation #mz view -= #az view
# 대쉬 방향용: 지금 누르고 있는 이동 방향(단위 벡터 × 1000)
scoreboard players set #inAct view 1
scoreboard players operation #inx view = #mx view
scoreboard players operation #inz view = #mz view
# 달리기 시야 효과
scoreboard players set #sprNow view 0
execute if score #f view matches 1 if predicate rlk:in_sprint run scoreboard players set #sprNow view 1
# 평타를 휘두르는 동안(swHold): 누른 방향은 대쉬 방향(#inx/#inz)으로만 쓰고 아바타는 걷지 않는다. 걷던 속도는 휘두르기 시작한 틱에
# player/swing/tick 이 지웠고(stop_h), 그 뒤에 받은 넉백 · 떨어지기 · 동작의 전진(stepT)은 그대로 적용된다.
# 달리기 시야 효과(#sprNow)는 그대로 두어 휘두를 때마다 시야가 출렁이지 않게 한다.
execute if score @s swHold matches 1 run return 0
# 속도(칸/틱 × 10000) = #viewWalk × 이동 속도% (달리기 ×1.3)
scoreboard players operation #sp view = #viewWalk tmp
scoreboard players operation #sp view *= @s moveSpeed
scoreboard players operation #sp view /= #100 tmp
execute if score #f view matches 1 if predicate rlk:in_sprint run scoreboard players operation #sp view *= #viewSprint tmp
execute if score #f view matches 1 if predicate rlk:in_sprint run scoreboard players operation #sp view /= #100 tmp
execute if score @s bowT matches 1.. run scoreboard players operation #sp view *= #bowSlow tmp
execute if score @s bowT matches 1.. run scoreboard players operation #sp view /= #100 tmp
execute if score @s skDash matches 1.. run scoreboard players operation #sp view *= #skDashSpd tmp
execute if score @s skDash matches 1.. run scoreboard players operation #sp view /= #100 tmp
scoreboard players operation #mx view *= #sp view
scoreboard players operation #mx view /= #1000 tmp
scoreboard players operation #mz view *= #sp view
scoreboard players operation #mz view /= #1000 tmp
execute store result entity @e[tag=rlk_av,limit=1] Motion[0] double 0.0001 run scoreboard players get #mx view
execute store result entity @e[tag=rlk_av,limit=1] Motion[2] double 0.0001 run scoreboard players get #mz view
