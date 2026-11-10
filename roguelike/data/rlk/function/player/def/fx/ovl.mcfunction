# {g,in,hold,out,t}: a full-screen glyph (g/title) unless another big title (vBig: a boss kit's overlay, the earlier parry
# streak) or a bottom line (ttlT: dialogue, notices) is up — changing the title times would cut that text short
execute if entity @a[tag=player,scores={vBig=1..},limit=1] run return 0
execute if entity @a[tag=player,scores={ttlT=1..},limit=1] run return 0
$function rlk:player/def/fx/g/title {g:"$(g)",in:$(in),hold:$(hold),out:$(out),t:$(t)}
