from enum import Enum
from typing import Dict, List, Tuple


class QuizTypeEnum(Enum):
    ''' Typ quizu:
        * STD - Każdy podaje swoją propozycję, która jest pokazywana na koniec.
        * RACE - Pierwsza osoba która się zgłosi odpowiada. Jeśli nie trafi minusowy punkt i szansa dla innych.

        Poprawność oceniana jest większościowo przez uczestników.
    '''
    STD = 1
    RACE = 2


class Participant:
    ''' Zbiera ocenione głosy oddane przez uczestnika.
    '''

    def __init__(self, name: str) -> None:
        self.name = name
        self.votes: List[Tuple[str, bool]] = []

    def get_summary(self) -> Tuple[List[str], List[str]]:
        ''' Zwraca wybory gracza, 1 - poprawne, 2 - niepoprawne
        '''
        return [song for song, result in self.votes if result], [song for song, result in self.votes if not result]

    def get_points(self, qtype: QuizTypeEnum) -> int:
        points = []

        for _song, result in self.votes:
            if result:
                points.append(1)

            elif qtype == QuizTypeEnum.RACE:
                points.append(-1)

        return sum(points)


class Quiz:
    def __init__(self,
                 qtype: QuizTypeEnum,
                 name: str,
                 playlist: str,
                 song_count: int) -> None:

        self.qtype = qtype
        self.name = name
        self.playlist = playlist
        self.songs_left = song_count

        self.participants: List[Participant] = []

    def next_round(self, votes: Dict[str, Tuple[str, bool]]) -> bool:
        for p in self.participants:
            try:
                p.votes.append(votes[p.name])
            except KeyError:
                pass

        self.songs_left -= 1

        if self.songs_left == 0:
            return False

        return True

    def summary(self) -> List[Participant]:
        return sorted(self.participants, key=lambda p: p.get_points(self.qtype))

    def __repr__(self) -> str:
        return f'{self.name} - {self.qtype.name}'
