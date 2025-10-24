"""Reference Qur'an passages shipped with the demo application."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Passage:
    """A short Qur'an excerpt with metadata for the UI."""

    id: str
    surah: str
    ayah_range: str
    arabic_text: str
    transliteration: str
    translation_tr: str


PASSAGES: List[Passage] = [
    Passage(
        id="al-fatiha-1-7",
        surah="Fâtiha Suresi",
        ayah_range="1-7",
        arabic_text=(
            "\u0628\u0650\u0633\u0652\u0645ِ \u0627\u0644\u0644\u0651\u064e\u0647ِ "
            "\u0627\u0644\u0631\u0651\u064e\u062d\u0652\u0645\u064e\u0646ِ "
            "\u0627\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645ِ "
            "\u0627\u0644\u062d\u064e\u0645\u0652\u062fُ \u0644\u0644\u0651\u0647ِ "
            "\u0631\u064e\u0628\u0651ِ \u0627\u0644\u0639\u064e\u0627\u0644\u064e\u0645\u0650\u064a\u0646َ "
            "\u0627\u0644\u0631\u0651\u064e\u062d\u0652\u0645\u064e\u0646ِ "
            "\u0627\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645ِ "
            "\u0645\u064e\u0627\u0644\u0650\u0643ِ \u064a\u064e\u0648\u0652\u0645ِ "
            "\u0627\u0644\u062f\u0651\u0650\u064a\u0652\u0646ِ \u0625\u0650\u064a\u064e\u0627\u0643َ "
            "\u0646\u064e\u0639\u0652\u0628\u064f\u062fُ \u0648\u0625\u0650\u064a\u064e\u0627\u0643َ "
            "\u0646\u064e\u0633\u0652\u062a\u064e\u0639\u0650\u064a\u0646ُ \u0627\u0647\u0652\u062fِ\u0646\u064e\u0627 "
            "\u0627\u0644\u0635\u0651\u0650\u0631\u064e\u0627\u0637َ \u0627\u0644\u0652\u0645\u064f\u0633\u0652\u062a\u064e\u0642\u0650\u064a\u0645َ "
            "\u0635\u0650\u0631\u064e\u0627\u0637َ \u0627\u0644\u0651\u064e\u0630\u0650\u064a\u0652\u0646َ "
            "\u0623\u064e\u0646\u0652\u0639\u064e\u0645\u0652\u062aَ \u0639\u064e\u0644\u064e\u064a\u0647\u0650\u0645ْ "
            "\u063a\u064e\u064a\u0652\u0631ِ \u0627\u0644\u0652\u0645\u064e\u063a\u0652\u0636\u064f\u0648\u0628ِ "
            "\u0639\u064e\u0644\u064e\u064a\u0652\u0647\u0650\u0645ْ \u0648\u064e\u0644\u064e\u0627 "
            "\u0627\u0644\u0636\u0651\u064e\u0627\u0644\u0651\u0650\u064a\u0652\u0646َ"
        ),
        transliteration=(
            "Bismillâhirrahmânirrahîm. Elhamdü lillâhi rabbil âlemîn. "
            "Errahmânirrahîm. Mâliki yevmiddîn. İyyâke na'budu ve iyyâke "
            "nestain. İhdinessırâtal mustakîm. Sırâtallezîne en'amte aleyhim "
            "ğayril mağdûbi aleyhim veleddâllîn."
        ),
        translation_tr=(
            "Rahmân ve Rahîm olan Allah'ın adıyla. Hamd, âlemlerin Rabbi Allah'a "
            "mahsustur. O, Rahmân ve Rahîm'dir. Din gününün sahibidir. "
            "(Allah'ım!) Ancak Sana ibadet eder ve ancak Senden yardım dileriz. "
            "Bizi dosdoğru yola ilet; Kendilerine nimet verdiklerinin yoluna; "
            "Gazaba uğrayanlarınkine ve sapmışlarınkine değil."
        ),
    ),
    Passage(
        id="al-ikhlas-1-4",
        surah="İhlâs Suresi",
        ayah_range="1-4",
        arabic_text=(
            "\u0642\u064f\u0644\u0652 \u0647\u064f\u0648\u064e \u0627\u0644\u0644\u0647ُ "
            "\u0623\u064e\u062d\u064e\u062fٌ \u0627\u0644\u0644\u0647ُ \u0627\u0644\u0635\u0651\u064e\u0645\u064e\u062fُ "
            "\u0644\u064e\u0645\u0652 \u064a\u064e\u0644\u0650\u062fْ \u0648\u064e\u0644\u064e\u0645ْ "
            "\u064a\u064f\u0648\u0644\u064e\u062fْ \u0648\u064e\u0644\u064e\u0645ْ \u064a\u064f\u0643\u064f\u0646ْ "
            "\u0644\u064e\u0647ُ \u0643\u064f\u0641\u064f\u0648\u064b\u0627 \u0623\u064e\u062d\u064e\u062fٌ"
        ),
        transliteration=(
            "Kul huvallâhu ehad. Allahus-samed. Lem yelid ve lem yûled. "
            "Ve lem yekun lehu kufuven ehad."
        ),
        translation_tr=(
            "De ki: O Allah birdir. Allah Samed'dir (her şey O'na muhtaçtır, O hiç kimseye muhtaç değildir). "
            "Doğurmamış ve doğurulmamıştır. Hiçbir şey O'na denk değildir."
        ),
    ),
]


class PassageRepository:
    """Utility helpers to look up reference passages."""

    def __init__(self, passages: Optional[List[Passage]] = None) -> None:
        self._passages = passages or PASSAGES
        self._by_id: Dict[str, Passage] = {passage.id: passage for passage in self._passages}

    def all(self) -> List[Passage]:
        return list(self._passages)

    def get(self, passage_id: str) -> Passage:
        if passage_id not in self._by_id:
            raise KeyError(f"Passage '{passage_id}' not found")
        return self._by_id[passage_id]
