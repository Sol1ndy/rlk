# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.old_slate set value {item:"minecraft:smooth_stone_slab",name:"낡은 석판",type:"accessory",rarity:"rare",stats:{},abilities:[{text:"",extra:[{text:"인벤토리에서 이 아이템의 양옆 칸에 있는"}]},{text:"",extra:[{text:"아이템의 스탯이 증가한다."}]},{text:""},{text:"",extra:[{text:"스탯 증가: "},{text:"30%",color:"#FFE08A"}]}],desc:["무엇이 적혀 있었는지는 아무도 모른다."],engravings:["petra","treasure"]}
data modify storage rlk:items ids append value "old_slate"
