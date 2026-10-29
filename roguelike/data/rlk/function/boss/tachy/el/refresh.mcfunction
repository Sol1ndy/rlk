# G1 aura refresh (every 20 t from core/fight, @s = body): the current element back to 1U when below
# 400 (a reaction consumed it); elAct 1 keeps the element tick on her.
scoreboard players set #aut tk 0
execute if score #el tk matches 1 if score @s aFire matches ..399 run scoreboard players set @s aFire 1000
execute if score #el tk matches 3 if score @s aThunder matches ..399 run scoreboard players set @s aThunder 1000
scoreboard players set @s elAct 1
