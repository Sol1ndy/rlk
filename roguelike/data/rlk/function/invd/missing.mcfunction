# 사본(커서·다른 칸)을 지우고 제자리에 다시 둔다. 지운 것이 있었으면 누른 것
execute store result score #t1 itv run clear @s *[minecraft:custom_data~{rlk_invd:1b}]
item replace entity @s inventory.2 with minecraft:chest[minecraft:item_name={text:"◆ 인벤토리 상세",color:"#FFE08A",bold:true},minecraft:lore=[{text:"클릭하면 아이템 정리 공간으로 이동합니다.",color:"white",italic:false},{text:"아이템 순서 바꾸기 · 판매",color:"gray",italic:false},{text:"전투 중에는 쓸 수 없습니다.",color:"dark_gray",italic:false}],minecraft:custom_data={rlk_invd:1b}]
execute if score #t1 itv matches 1.. at @s run function rlk:invd/open
