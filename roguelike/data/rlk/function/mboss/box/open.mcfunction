# From room/obj/do_mbox on the FIRST click of a box (@s = its object marker, at @s), after its pick was granted.
# The box stays where it is until a mid-boss pick is used (box/spend): backing out of the screen with Shift leaves
# it, and a later click only reopens the screen. oarg = open age (closed 0; the newest opened box 1, older ones
# count up), so box/spend takes the oldest. Every entity of its group gets rlk_mb_boxopen; the chest gets a gold
# outline, the label "(열림)". No global counter: room/clear and uninstall remove the tags with the entities.
scoreboard players add @e[type=minecraft:marker,tag=rlk_obj,tag=rlk_mb_boxopen] oarg 1
scoreboard players set @s oarg 1
scoreboard players operation #mbBoxG mb = @s ogid
execute as @e[tag=rlk_room] if score @s ogid = #mbBoxG mb run tag @s add rlk_mb_boxopen
execute as @e[type=minecraft:item_display,tag=rlk_mb_box,tag=rlk_mb_boxopen] if score @s ogid = #mbBoxG mb run data merge entity @s {Glowing:1b,glow_color_override:16765514}
execute as @e[type=minecraft:text_display,tag=rlk_olbl,tag=rlk_mb_boxopen] if score @s ogid = #mbBoxG mb run data modify entity @s text set value [{text:"아이템 상자",color:"#FFD24A",bold:true},{text:"\n(열림)",color:"#FFE08A",bold:true},{text:"\n다시 눌러 선택",color:"#D0D0D0",bold:false}]
