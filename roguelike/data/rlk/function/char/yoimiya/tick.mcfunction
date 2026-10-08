# 요이미야 매 틱 (@s = 플레이어, at 몸): 스킬 지속 · 소매불 · 유금화광 표시
execute if score @s yoiPcCd matches 1.. run scoreboard players remove @s yoiPcCd 1
execute if score #yoiBoomCd tmp matches 1.. run scoreboard players remove #yoiBoomCd tmp 1
execute if score @s yoiSk matches 1.. run function rlk:char/yoimiya/skill_tick
execute unless score @s yoiSk matches 1.. run scoreboard players reset 염초정화 stacks
execute if score @s yoiPT matches 1.. run scoreboard players remove @s yoiPT 1
execute if score @s yoiPT matches 0 run scoreboard players set @s yoiP 0
execute if score @s yoiP matches 1.. run scoreboard players operation 소매불 stacks = @s yoiP
execute if score @s yoiP matches 1.. run scoreboard players display name 소매불 stacks {text:"소매불 백경도",color:"#FF8A3D"}
execute unless score @s yoiP matches 1.. run scoreboard players reset 소매불 stacks
# 유금화광이 붙은 적: 머리 위 불꽃
execute store result score #ynow tmp run time query gametime
execute as @e[tag=rlk_mob] if score @s aurEnd > #ynow tmp at @s run particle minecraft:dust{color:[1.0f,0.75f,0.2f],scale:1.1f} ~ ~2.3 ~ 0.12 0.08 0.12 0 1
