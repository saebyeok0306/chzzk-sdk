from dataclasses import dataclass


@dataclass
class Credential:
    """
    auth: NID_AUT
    session: NID_SES
    """
    auth: str
    session: str

    def as_cookie(self) -> dict[str, str]:
        return {
            "NID_AUT": self.auth,
            "NID_SES": self.session
        }