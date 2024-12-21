from .const import HEXAGRAM_DESCRIPTION_STR

_乾 = HEXAGRAM_DESCRIPTION_STR["乾"]
_兑 = HEXAGRAM_DESCRIPTION_STR["兑"]
_离 = HEXAGRAM_DESCRIPTION_STR["离"]
_震 = HEXAGRAM_DESCRIPTION_STR["震"]
_巽 = HEXAGRAM_DESCRIPTION_STR["巽"]
_坎 = HEXAGRAM_DESCRIPTION_STR["坎"]
_艮 = HEXAGRAM_DESCRIPTION_STR["艮"]
_坤 = HEXAGRAM_DESCRIPTION_STR["坤"]

NAME_TO_HEXAGRAMS_64 = {
    "乾为天": (_乾, _乾),
    "坤为地": (_坤, _坤),
    "水雷屯": (_坎, _震),
    "山水蒙": (_艮, _坎),
    "水天需": (_坎, _乾),
    "天水讼": (_乾, _坎),
    "地水师": (_坤, _坎),
    "水地比": (_坎, _坤),
    "风天小畜": (_巽, _乾),
    "天泽履": (_乾, _兑),
    "地天泰": (_坤, _乾),
    "天地否": (_乾, _坤),
    "天火同人": (_乾, _离),
    "火天大有": (_离, _乾),
    "地山谦": (_坤, _艮),
    "雷地豫": (_震, _坤),
    "泽雷随": (_兑, _震),
    "山风蛊": (_艮, _巽),
    "地泽临": (_坤, _兑),
    "风地观": (_巽, _坤),
    "火雷噬嗑": (_离, _震),
    "山火贲": (_艮, _离),
    "山地剥": (_艮, _坤),
    "地雷复": (_坤, _震),
    "天雷无妄": (_乾, _震),
    "山天大畜": (_艮, _乾),
    "山雷颐": (_艮, _震),
    "泽风大过": (_兑, _巽),
    "坎为水": (_坎, _坎),
    "离为火": (_离, _离),
    "泽山咸": (_兑, _艮),
    "雷风恒": (_震, _巽),
    "天山遁": (_乾, _艮),
    "雷天大壮": (_震, _乾),
    "火地晋": (_离, _坤),
    "地火明夷": (_坤, _离),
    "风火家人": (_巽, _离),
    "火泽睽": (_离, _兑),
    "水山蹇": (_坎, _艮),
    "雷水解": (_震, _坎),
    "山泽损": (_艮, _兑),
    "风雷益": (_巽, _震),
    "泽天夬": (_兑, _乾),
    "天风姤": (_乾, _巽),
    "泽地萃": (_兑, _坤),
    "地风升": (_坤, _巽),
    "泽水困": (_兑, _坎),
    "水风井": (_坎, _巽),
    "泽火革": (_兑, _离),
    "火风鼎": (_离, _巽),
    "震为雷": (_震, _震),
    "艮为山": (_艮, _艮),
    "风山渐": (_巽, _艮),
    "雷泽归妹": (_震, _兑),
    "雷火丰": (_震, _离),
    "火山旅": (_离, _艮),
    "巽为风": (_巽, _巽),
    "兑为泽": (_兑, _兑),
    "风水涣": (_坎, _巽),
    "水泽节": (_兑, _坎),
    "风泽中孚": (_巽, _兑),
    "雷山小过": (_震, _艮),
    "水火既济": (_坎, _离),
    "火水未济": (_离, _坎)
}

HEXAGRAMS_64_TO_NAME = {tuple(hexagrams): name for name, hexagrams in NAME_TO_HEXAGRAMS_64.items()}