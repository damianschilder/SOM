from typing import List

class Tariefeenheden:

    @staticmethod
    def get_stations() -> List[str]:
        return ["Utrecht Centraal",
                "Gouda",
                "Geldermalsen",
                "Hilversum",
                "Duivendrecht",
                "Weesp"]

    @staticmethod
    def get_tariefeenheden(frm: str, to: str) -> int:
        if frm == "Utrecht Centraal":
            if to == "Utrecht Centraal":
                return 0
            elif to == "Gouda":
                return 32
            elif to == "Geldermalsen":
                return 26
            elif to == "Hilversum":
                return 18
            elif to == "Duivendrecht":
                return 31
            elif to == "Weesp":
                return 33
            else:
                raise Exception("Unknown stations")

        elif frm == "Gouda":
            if to == "Gouda":
                return 0
            elif to == "Geldermalsen":
                return 58
            elif to == "Hilversum":
                return 50
            elif to == "Duivendrecht":
                return 54
            elif to == "Weesp":
                return 57
            else:
                return Tariefeenheden.get_tariefeenheden(to, frm)

        elif frm == "Geldermalsen":
            if to == "Geldermalsen":
                return 0
            elif to == "Hilversum":
                return 44
            elif to == "Duivendrecht":
                return 57
            elif to == "Weesp":
                return 59
            else:
                return Tariefeenheden.get_tariefeenheden(to, frm)

        elif frm == "Hilversum":
            if to == "Hilversum":
                return 0
            elif to == "Duivendrecht":
                return 18
            elif to == "Weesp":
                return 15
            else:
                return Tariefeenheden.get_tariefeenheden(to, frm)

        elif frm == "Duivendrecht":
            if to == "Duivendrecht":
                return 0
            elif to == "Weesp":
                return 3
            else:
                return Tariefeenheden.get_tariefeenheden(to, frm)

        elif frm == "Weesp":
            if to == "Weesp":
                return 0
            else:
                return Tariefeenheden.get_tariefeenheden(to, frm)
        
        else:
            raise Exception("Unknown stations")
