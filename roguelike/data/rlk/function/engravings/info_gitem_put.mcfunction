# 각인이 여럿인 묶음: 이름 = "◆ 첫 각인 외 k종  n개"
$item replace entity @s inventory.$(slot) with $(icon)[minecraft:item_name={text:"◆ $(name)",color:"$(color)",bold:true,extra:[{text:" 외 $(more)종",color:"gray",bold:false},{text:"  $(n)개",color:"white",bold:false}]},minecraft:lore=$(lore),minecraft:custom_data={rlk_engi:1b},minecraft:max_stack_size=99] $(cnt)
