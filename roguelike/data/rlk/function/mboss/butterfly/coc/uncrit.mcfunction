# A forced crit (engravings: 6 keen, frost) on the body while CRIT -100 %: back to a normal hit (x 100 / crit
# damage), shown as a normal number. Roll-based crits never happen (critChance -100 in items/hook/stat_buffs).
scoreboard players set #crit tmp 0
execute unless score @a[tag=player,limit=1] critDamage matches 101.. run return 0
scoreboard players operation #dmg tmp *= #c100 mb
scoreboard players operation #dmg tmp /= @a[tag=player,limit=1] critDamage
execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1
