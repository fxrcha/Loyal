import plistlib
from utils.request import Base

MESU_APPLE = "https://mesu.apple.com/assets"
ITUNES_SERVER = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/com.apple.jingle.appserver.client.MZITunesClientCheck/version"


WatchOSXML = "/watch/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml"
tvOSXML = (
    "/tv/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml"
)
iOSXML = (
    "/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml"
)
AudioOSXML = "/audio/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml"
iOSDeveloperXML = "/iOS<version>DeveloperSeed/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml"
iOSPublicXML = "/iOS<version>PublicSeed/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml"

AudioDevices = [
    "A1523",  # AirPods (1st generation)
    "A2032",  # AirPods (2nd generation)
    "A2084",  # AirPods Pro
    "A2096",  # AirPods Max
    "A1796",  # Beats Solo3 Wireless
    "A1881",  # Beats Solo Pro
    "A1914",  # Beats Studio 3 Wireless
    "A1747",  # Beats X
    "A1763",  # PowerBeats 3
    "A2048",  # PowerBeats Pro
    "A2015",  # PowerBeats
]

Accesories = [
    "WirelessStylusFirmware",  # Apple Pencil (1st generation)
    "WirelessStylusFirmware_2",  # Apple Pencil (2nd generation)
    "KeyboardCoverFirmware",  # Smart Keyboard
    "KeyboardCoverFirmware_4",  # Smart Keyboard Folio (11-inch)
    "KeyboardCoverFirmware_5",  # Smart Keyboard Folio (12.9-inch)
]


class LoyalRequest(Base):
    def __init__(self) -> None:
        self.fields = {
            "watchOS": WatchOSXML,
            "tvOS": tvOSXML,
            "iOS": iOSXML,
            "audioOS": AudioOSXML,
            "iOSDB": iOSDeveloperXML,
            "iOSPB": iOSPublicXML,
        }
        super().__init__()

    async def itunes(self):
        resp = await self.get(ITUNES_SERVER)
        data = await resp.text(encoding="utf-8")

        return plistlib.loads(bytes(data, encoding="utf-8"))

    async def mesu(self, field):
        if not field == "custom":
            dest = self.fields[field]

        else:  # for cases of AirPods firmwares
            dest = field

        resp = await self.get(MESU_APPLE + dest)
        data = await resp.text(encoding="utf-8")

        return plistlib.loads(bytes(data, encoding="utf-8"))

    async def close_session(self):
        await self.session.close()