# Called as the mob after shields, only for positive direct damage.
# snd is cleared each game tick; cleaving several mobs cannot stack the thud.
scoreboard players set #confirmedHit snd 1
# Center this short contact feedback on the listener so the shoulder camera
# cannot attenuate it. The swing/element sounds remain at the attack location.
execute as @a[tag=player,limit=1] at @s run playsound minecraft:entity.player.attack.knockback player @s ~ ~ ~ 0.85 0.68 0
execute as @a[tag=player,limit=1] at @s run playsound minecraft:block.note_block.basedrum player @s ~ ~ ~ 0.52 0.62 0
execute if score #crit tmp matches 1 as @a[tag=player,limit=1] at @s run playsound minecraft:entity.player.attack.crit player @s ~ ~ ~ 0.4 0.78 0
