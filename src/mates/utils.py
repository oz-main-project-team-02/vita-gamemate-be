GAME_LEVEL_CHOICES = {
    1: [
        ("챌린저", "챌린저"),
        ("그랜드 마스터", "그랜드 마스터"),
        ("마스터", "마스터"),
        ("다이아몬드", "다이아몬드"),
        ("에메랄드", "에메랄드"),
        ("플래티넘", "플래티넘"),
        ("골드", "골드"),
        ("실버", "실버"),
        ("브론즈", "브론즈"),
        ("아이언", "아이언"),
    ],
    2: [
        ("챔피언", "챔피언"),
        ("그랜드 마스터", "그랜드 마스터"),
        ("마스터", "마스터"),
        ("다이아몬드", "다이아몬드"),
        ("에메랄드", "에메랄드"),
        ("플래티넘", "플래티넘"),
        ("골드", "골드"),
        ("실버", "실버"),
        ("브론즈", "브론즈"),
    ],
    3: [
        ("챌린저", "챌린저"),
        ("그랜드 마스터", "그랜드 마스터"),
        ("마스터", "마스터"),
        ("다이아몬드", "다이아몬드"),
        ("에메랄드", "에메랄드"),
        ("플래티넘", "플래티넘"),
        ("골드", "골드"),
        ("실버", "실버"),
        ("브론즈", "브론즈"),
        ("아이언", "아이언"),
    ],
    4: [
        ("마스터", "마스터"),
        ("다이아몬드", "다이아몬드"),
        ("플래티넘", "플래티넘"),
        ("골드", "골드"),
        ("실버", "실버"),
        ("브론즈", "브론즈"),
    ],
}

from rest_framework.pagination import PageNumberPagination


class MateGameInfoPagination(PageNumberPagination):
    page_size = 30