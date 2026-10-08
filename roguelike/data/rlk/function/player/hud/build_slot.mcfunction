# #hi 번째 칸(0부터): 충전 수보다 작으면 완료 칸, 같으면 충전 중인 칸, 크면 빈 칸
execute if score #hi tmp >= #dashMax tmp run return 0
execute if score #hi tmp < @s dashCharge run data modify storage rlk:hud line append from storage rlk:hud full
execute if score #hi tmp = @s dashCharge run function rlk:player/hud/part with storage rlk:hud
execute if score #hi tmp > @s dashCharge run data modify storage rlk:hud line append from storage rlk:hud part[0]
scoreboard players add #hi tmp 1
function rlk:player/hud/build_slot
