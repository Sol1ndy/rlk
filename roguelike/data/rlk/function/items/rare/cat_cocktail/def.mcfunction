# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.cat_cocktail set value {item:"minecraft:honey_bottle",name:"고양이 꼬리 칵테일",type:"accessory",rarity:"rare",stats:{hpPct:8},abilities:[{text:"",extra:[{text:"보호막이 있는 동안 이동 속도와 공격 속도가 증가한다."}]},{text:""},{text:"",extra:[{text:"이동 속도 증가: "},{text:"10%",color:"#FFE08A"}]},{text:"",extra:[{text:"공격 속도 증가: "},{text:"10%",color:"#FFE08A"}]}],desc:["술은 싫지만 만드는 건 잘한다."],engravings:["guard","dash"]}
data modify storage rlk:items ids append value "cat_cocktail"
