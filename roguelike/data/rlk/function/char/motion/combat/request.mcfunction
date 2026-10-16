execute if score #charN tmp matches 3 if score @s skDash matches 1.. run return 0
execute if score @s rdCam matches 1 run return 0
# Queue a genuine hit at the recorded blade-contact frame; keep all existing damage/buff rules.
execute if score @s pmMoveLock matches 1 run return 0
execute if score @s arSk matches 1.. run return 0
execute if score @s skBurst matches 1.. run return 0
execute if score @s dashMoveT matches 1.. run return 0
# Navia: no normal attack while aiming the parasol gun.
execute if score #charN tmp matches 6 if score @s nvA matches 1.. run return 0
execute if score @s comboStep matches ..-1 run scoreboard players set @s comboStep 0
execute if score #charN tmp matches 5 if score @s comboStep matches 6.. run scoreboard players set @s comboStep 0
execute if score #charN tmp matches 3 if score @s comboStep matches 5.. run scoreboard players set @s comboStep 0
execute if score #charN tmp matches 6 if score @s comboStep matches 4.. run scoreboard players set @s comboStep 0
scoreboard players operation @s pmAtkStep = @s comboStep
scoreboard players operation @s pmAtkKind = #charN tmp
scoreboard players set @s skQ 0
scoreboard players set @s naQ 0
scoreboard players set @s naQn 0
function rlk:char/motion/combat/select
function rlk:char/motion/combat/config with storage rlk:player_motion active
scoreboard players set @s pmAtkPending 1
# Next-combo cadence follows reference footage and scales with attack speed.
scoreboard players operation @s atkCD = @s pmChain
scoreboard players operation @s atkCD *= #100 tmp
scoreboard players operation @s atkCD += @s pmSpeed
scoreboard players remove @s atkCD 1
scoreboard players operation @s atkCD /= @s pmSpeed
execute if score @s atkCD matches ..1 run scoreboard players set @s atkCD 2
scoreboard players operation @s vAimT = @s atkCD
scoreboard players set @s cboIdle 0
execute store result score @s swungAt run time query gametime
