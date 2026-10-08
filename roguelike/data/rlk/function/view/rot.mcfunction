# 카메라 자리 잡기 (@s = 플레이어). 시선을 표식(rlk_vmk)에 옮겨 적어 읽는다(플레이어 NBT 를 직접 읽는 것보다 가벼움)
execute rotated as @s as @e[tag=rlk_vmk,limit=1] run rotate @s ~ ~
execute store result score #yw view run data get entity @e[tag=rlk_vmk,limit=1] Rotation[0] 100
execute store result score #pt view run data get entity @e[tag=rlk_vmk,limit=1] Rotation[1] 100
# 이번 틱 변화량
scoreboard players operation #dy view = #yw view
scoreboard players operation #dy view -= @s vYaw
scoreboard players operation #dp view = #pt view
scoreboard players operation #dp view -= @s vPitch
scoreboard players operation @s vYaw = #yw view
scoreboard players operation @s vPitch = #pt view
execute if score #dy view matches 18000.. run scoreboard players remove #dy view 36000
execute if score #dy view matches ..-18000 run scoreboard players add #dy view 36000
# 고르게 펴기: 지난 틱 변화량의 절반을 더한다(±#viewEven 까지)
scoreboard players operation #ey view = @s vDy
scoreboard players operation #ey view /= #2 tmp
execute if score #ey view > #viewEven tmp run scoreboard players operation #ey view = #viewEven tmp
scoreboard players operation #evn view = #viewEven tmp
scoreboard players operation #evn view *= #neg1 tmp
execute if score #ey view < #evn view run scoreboard players operation #ey view = #evn view
scoreboard players operation #ep view = @s vDp
scoreboard players operation #ep view /= #2 tmp
execute if score #ep view > #viewEven tmp run scoreboard players operation #ep view = #viewEven tmp
execute if score #ep view < #evn view run scoreboard players operation #ep view = #evn view
scoreboard players operation @s vDy = #dy view
scoreboard players operation @s vDp = #dp view
scoreboard players operation #cy view = #yw view
scoreboard players operation #cy view += #ey view
scoreboard players operation #cp view = #pt view
scoreboard players operation #cp view += #ep view
# 회전 예측(view/tune 의 lead): 이번 틱 좌우 변화량 × lead (한 틱 40도까지)
execute if score #lead view matches 1.. run function rlk:view/rot_lead
execute if score #cp view matches 9000.. run scoreboard players set #cp view 9000
execute if score #cp view matches ..-9000 run scoreboard players set #cp view -9000
execute store result storage rlk:view pr.y double 0.01 run scoreboard players get #cy view
execute store result storage rlk:view pr.p double 0.01 run scoreboard players get #cp view
# 보간 틱 수가 설정과 다르면 맞춤
# 대쉬 중·직후에는 아바타와 같은 틱 수로(#viewDashDur), 그 밖에는 설정(smooth)대로
scoreboard players operation #durWant view = #durFast view
execute if score @s dashMoveT matches 1.. run scoreboard players operation #dashCam view = #viewDashHold tmp
execute if score #dashCam view matches 1.. run scoreboard players remove #dashCam view 1
execute if score #dashCam view matches 1.. if score #durWant view < #viewDashDur tmp run scoreboard players operation #durWant view = #viewDashDur tmp
execute unless score #durNow view = #durWant view run function rlk:view/dur_set
# 카메라 높이(점프할 때 덜 따라가게)
function rlk:view/cam_y
function rlk:view/cam_go with storage rlk:view pr
