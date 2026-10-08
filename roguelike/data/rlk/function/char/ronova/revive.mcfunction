# 불사의 저주 발동 (@s = 플레이어, 체력 0): 맵마다 한 번. #rnDieT 틱 동안 쓰러져 있다가 최대 체력의 #rnRevPct% 로 되살아난다
# 걸려 있던 버프(방어막 · 원소 부여 · 이로운 효과)는 사라진다. 쓰러져 있는 동안: 움직임·공격·스킬 불가, 어둠, 무적, 체력 바가 점점 차오름
scoreboard players set @s rnRev 1
scoreboard players operation @s rnDie = #rnDieT tmp
scoreboard players set @s curHealth 1
scoreboard players set @s shieldHP 0
scoreboard players set @s shieldT 0
function rlk:element/infuse_end
effect clear @s minecraft:speed
effect clear @s minecraft:strength
effect clear @s minecraft:regeneration
effect clear @s minecraft:resistance
effect clear @s minecraft:absorption
effect clear @s minecraft:jump_boost
effect clear @s minecraft:haste
effect give @s minecraft:darkness 5 0 true
# 쓰러져 있는 동안 + 일어난 뒤 1초 무적
scoreboard players operation @s dashInvT = #rnDieT tmp
scoreboard players add @s dashInvT 20
scoreboard players set @s dashMoveT 0
attribute @s minecraft:movement_speed modifier remove rlk:ronova_die
attribute @s minecraft:movement_speed modifier add rlk:ronova_die -1 add_multiplied_total
attribute @s minecraft:jump_strength modifier remove rlk:ronova_die
attribute @s minecraft:jump_strength modifier add rlk:ronova_die -1 add_multiplied_total
function rlk:view/stop_h
execute as @e[tag=rlk_av,limit=1] run data modify entity @s pose set value "sleeping"
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.88,0.12,0.22],scale:2.0} ~ ~0.5 ~ 0.6 0.3 0.6 0 40
execute at @e[tag=rlk_body,limit=1] run particle minecraft:squid_ink ~ ~0.5 ~ 0.4 0.2 0.4 0.05 20
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.death master @a ~ ~ ~ 0.8 0.8
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.bell.use master @a ~ ~ ~ 0.6 0.5
