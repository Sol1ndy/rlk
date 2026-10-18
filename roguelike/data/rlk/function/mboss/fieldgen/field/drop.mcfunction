# The field state ends without its sequence (pack-up done, the break, a reload): stage 0, the next field after
# 4 cruise patterns, meter / low gravity / cut off, the cruise hitbox.
scoreboard players set #fgField mb 0
scoreboard players set #fgWvK mb 0
scoreboard players set #fgFT mb 0
scoreboard players set #fgOpen mb 0
scoreboard players set #fgLowG mb 0
scoreboard players set #fgCruN mb 0
scoreboard players set #fgCruLim mb 4
function rlk:mboss/fieldgen/form/hitbox_c
function rlk:mboss/fieldgen/hud/refresh
