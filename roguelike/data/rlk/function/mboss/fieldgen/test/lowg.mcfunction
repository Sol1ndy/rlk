# Low gravity on / off by hand (the jump check in both views); the field sets it again at its banner.
scoreboard players set #fgX mb 1
execute if score #fgLowG mb matches 1 run scoreboard players set #fgX mb 0
scoreboard players operation #fgLowG mb = #fgX mb
execute if score #fgLowG mb matches 1 run function rlk:mboss/fieldgen/fx/hud/lowg_on
execute if score #fgLowG mb matches 0 run function rlk:mboss/fieldgen/fx/hud/lowg_off
execute if score #fgLowG mb matches 1 run tellraw @a[tag=player] {text:"[테스트] 저중력 켬",color:"gray"}
execute if score #fgLowG mb matches 0 run tellraw @a[tag=player] {text:"[테스트] 저중력 끔",color:"gray"}
