# Butterfly form: time left before 달빛 해제 (or fewer patterns).
scoreboard players set #buSub bu 900
scoreboard players operation #buSub bu -= #bfBfT mb
execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0
scoreboard players set #buSubMax bu 900
scoreboard players set #buSubCol bu 7
