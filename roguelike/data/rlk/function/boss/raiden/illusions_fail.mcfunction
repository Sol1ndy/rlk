function rlk:boss/raiden/object/clear
scoreboard players set @s rdAnim 8
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/raiden/hazard/create {shape:6,tell:24,damage:26,life:34}
# Pattern names intentionally stay out of the boss bar.
