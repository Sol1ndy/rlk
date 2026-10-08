# @s = 레벨 글자 (macro: lv). 레벨이 바뀌었을 때만 다시 씀
$data modify entity @s text set value {text:"Lv.$(lv)",color:"#FFD86B",bold:true}
scoreboard players operation @s mlv = #lvNow tmp
