"""Raiden voice lines (typed subtitles) and the caption state. Owner: S2-SHOGUN (plan rd/plan.md E.0, D.2)."""
from .core import write

def typed(text):
    # Typewriter steps: each word grows at most two syllables at a time; punctuation
    # stays on its syllable, except the closing punctuation, which lands as the last step.
    PUNCT = '.,!?…'
    body = text.rstrip(PUNCT)
    tail = text[len(body):]
    steps, done = [], ''
    for w, word in enumerate(body.split(' ')):
        sylls = []
        for ch in word:
            if ch in PUNCT and sylls:
                sylls[-1] += ch
            else:
                sylls.append(ch)
        for k in range(0, len(sylls), 2):
            steps.append(done + ''.join(sylls[:k+2]))
        done = steps[-1] + ' '
    if tail:
        steps.append(text)
    return steps
# Boss lines from the original fight (나무위키 「마가츠 미타케 나루카미노 미코토」 3.2 패턴):
# key: (text or explicit steps, ticks per step, colour, hold of the full line)
VOICE, VOICE2 = '#d7b4ff', '#e6a3ff'
LINES = {
    'mangeop': (['그', '그 끝은', '그 끝은 만겁', '그 끝은 만겁일지니', '그 끝은 만겁일지니...'], 5, VOICE, 24),
    'eternal': ('이 몸이 곧 영원이다', 3, VOICE, 26),
    'nothing': ('그 무엇도 영원한 것은 없다.', 2, VOICE, 40),
    'eyes': ('뇌광이 영원의 땅을 비추는구나.', 2, VOICE, 24),
    'pohyeong': ('찰나의... 포영!', 3, VOICE, 22),
    'ganpa': ('간파했군.', 4, '#bfe4ff', 34),
    'noemyeong': ('뇌명.', 4, VOICE, 20),
    'will': ('뇌전은 인간의 의지 따위로 변하지 않아', 2, VOICE, 22),
    'command': ('번개여, 나의 호령을 따르라.', 2, VOICE, 22),
    'calm': ('무념 무상, 천하가 고요하리.', 2, VOICE, 12),
    'sever_one': ('무념 무상, 일도 단절.', 1, VOICE2, 16),
    'cleave_all': ('방해는 모두 베겠노라', 2, VOICE2, 22),
    'prison': ('감옥으로 만들어 주지', 2, VOICE2, 22),
    'cheonsu': ('천수의 속박!', 3, VOICE2, 30),
    'sever': ('단절!', 2, VOICE2, 20),
    'goemyeol': ('궤멸하라!', 3, VOICE2, 24),
    'pierce': ('뚫려라!', 2, VOICE2, 20),
}
LINE_IDS = {k: i for i, k in enumerate(LINES, 1)}


def build():
    # Boss captions ride on the HUD title timer: ttlT (subtitle lifetime, view/ride_tick
    # blanks the subtitle when it runs out so the 0.5 s crosshair title cannot replay it)
    # and vBig (pauses the crosshair while a big title is up). #rdCap marks a boss caption,
    # #rdCapPat one that belongs to the running pattern and ends with it.
    write('caption/expire','''
scoreboard players set #rdCap rd 0
scoreboard players set #rdCapPat rd 0
''')
    write('caption/clear','''
scoreboard players set #rdLine rd 0
execute unless score #rdCap rd matches 1 run return 0
function rlk:boss/raiden/caption/expire
title @a[tag=player] subtitle ""
scoreboard players set @a[tag=player,scores={ttlT=1..}] ttlT 0
scoreboard players set @a[tag=player,scores={vBig=1..}] vBig 0
''')
    tick_lines = ['# Advances the boss line in progress (#rdLine id, #rdLineT age); called from tick.',
                  'execute unless score #rdLine rd matches 1.. run return 0',
                  'scoreboard players add #rdLineT rd 1']
    for key, (steps, gap, colour, hold) in LINES.items():
        steps = typed(steps) if isinstance(steps, str) else steps
        lid = LINE_IDS[key]
        write('line/'+key, [f'scoreboard players set #rdLine rd {lid}', 'scoreboard players set #rdLineT rd -1'])
        for k, text in enumerate(steps):
            last = k == len(steps)-1
            stay = hold if last else gap+6
            # One plain, quiet tick per step (same sound and pitch every time).
            frame = [f'title @a[tag=player] times 0 {stay} {12 if last else 0}',
                     'title @a[tag=player] subtitle {text:"'+text+'",color:"'+colour+'",bold:true}',
                     'execute as @a[tag=player] run function rlk:view/ttl_blank',
                     f'scoreboard players set @a[tag=player] ttlT {stay+(12 if last else 0)}',
                     'scoreboard players set #rdCap rd 1', 'scoreboard players set #rdCapPat rd 1',
                     'execute as @a[tag=player] at @s run playsound minecraft:block.note_block.hat voice @s ~ ~ ~ .3 1 0']
            if last:
                frame.append('scoreboard players set #rdLine rd 0')
            write(f'line/{key}_{k}', frame)
            tick_lines.append(f'execute if score #rdLine rd matches {lid} if score #rdLineT rd matches {k*gap} run function rlk:boss/raiden/line/{key}_{k}')
    write('line/tick', tick_lines)
    write('caption/pattern_end','''
execute if score #rdCapPat rd matches 1 run function rlk:boss/raiden/caption/clear
''')
