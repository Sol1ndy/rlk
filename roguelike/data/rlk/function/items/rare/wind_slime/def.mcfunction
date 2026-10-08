# abilities = 설명 줄 목록(텍스트 컴포넌트). 형식: 효과 서술 → 빈 줄 → "항목: 수치"
data modify storage rlk:items registry.wind_slime set value {item:"minecraft:slime_ball",name:"바람 슬라임 인형",type:"accessory",rarity:"rare",stats:{elemMastery:40},abilities:[{text:"",extra:[{text:"확산 반응을 일으키면 한동안 원소 마스터리가 증가한다."}]},{text:""},{text:"",extra:[{text:"원소 마스터리 증가: "},{text:"80",color:"#FFE08A"}]},{text:"",extra:[{text:"지속 시간: "},{text:"8초",color:"#FFE08A"}]}],desc:["연금술 실험 제 육백 호의 결과물."],engravings:["amplify","lunar"]}
data modify storage rlk:items ids append value "wind_slime"
