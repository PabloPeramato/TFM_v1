import asyncio
from fastapi import APIRouter, HTTPException, Query
from app.api.routers import availability
from app.core.ssh_utils import run_command
from app.core.config import settings
from app.models.schemas import (
    StatusOK,
    PowerStatus,
    ListSerials
)
from app.utils.helpers import (
    send_mqtt_message,
    is_raspberry_pi_online,
    check_status_rpi
)


router = APIRouter()


@router.post("/on", tags=["power"])
def power_on(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        serial: str = Query(
            ...,
            description=(
                "Serial number of the Raspberry Pi to be powered on."
            )
        ),
        ) -> StatusOK:

    serial = serial.lower()

    hardware = availability.availability_hardware()
    unavailable = hardware.unavailable

    flag = False
    if unavailable != "[]":
        for rpi in unavailable:
            if serial == rpi.serial:
                if user == rpi.user:
                    flag = True
                    send_mqtt_message(serial, "OFF")
                    break
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"The user '{user}' does not have"
                            f" permission to power on the Raspberry Pi"
                            f" with serial '{serial}'."
                        )
                    )

        if flag is False:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"The Raspberry Pi with serial '{serial}'"
                    f" is not mounted, so it cannot be powered on."
                )
            )

    return StatusOK(
        status=200,
        message=(
            f"The Raspberry Pi with serial '{serial}' has successfully"
            f" powered on."
        )
    )


@router.post("/off", tags=["power"])
async def power_off(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        serial: str = Query(
            ...,
            description=(
                "Serial number of the Raspberry Pi to be powered off."
            )
        ),
        ) -> StatusOK:

    serial = serial.lower()

    if serial == "85d959ed":
        remote_host_raspi = settings.REMOTE_HOST_RPI3_85D9
        username_raspi = "root"
        password_raspi = settings.PASSWORD_PXE
    elif serial == "81b715b7":
        remote_host_raspi = settings.REMOTE_HOST_RPI3_81B7
        username_raspi = "root"
        password_raspi = settings.PASSWORD_PXE
    elif serial == "8ba14c83":
        remote_host_raspi = settings.REMOTE_HOST_RPI3_8BA1
        username_raspi = "root"
        password_raspi = settings.PASSWORD_PXE
    elif serial == "1718561b":
        remote_host_raspi = settings.REMOTE_HOST_RPI4_1718
        username_raspi = "root"
        password_raspi = settings.PASSWORD_PXE

    hardware = availability.availability_hardware()
    unavailable = hardware.unavailable

    flag = False
    if unavailable != "[]":
        for rpi in unavailable:
            if serial == rpi.serial:
                if user == rpi.user:
                    if is_raspberry_pi_online(remote_host_raspi):
                        run_command(
                            "sudo shutdown now",
                            remote_host_raspi,
                            username_raspi,
                            password_raspi
                        )
                        await asyncio.sleep(10)
                    flag = True
                    send_mqtt_message(serial, "ON")
                    break
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"The user '{user}' does not have"
                            f" permission to power off the Raspberry Pi"
                            f" with serial '{serial}'."
                        )
                    )

        if flag is False:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"The Raspberry Pi with serial '{serial}'"
                    f" is not mounted, so it cannot be powered off."
                )
            )

    return StatusOK(
        status=200,
        message=(
            f"The Raspberry Pi with serial '{serial}' has successfully"
            f" powered off."
        )
    )


# hacerlo con tokens, jwt, decrypt y autenticacion en fastapi
@router.get("/status", tags=["power"])
def power_status(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        ) -> PowerStatus:
    # admin muestra todas, usuario muestra solo las suyas
    rpi_power_status = []
    hardware = availability.availability_hardware()
    unavailable = hardware.unavailable

    if user == "admin":
        serials = settings.SERIAL_NUMBERS_3B + settings.SERIAL_NUMBERS_4B
        unavailable_serials = []

        for rpi in unavailable:
            list = ListSerials(
                serial=rpi.serial,
                os=rpi.os
            )
            unavailable_serials.append(list)

        for serial in serials:
            flag = False
            for element in unavailable_serials:
                if serial == element.serial:
                    flag = True
                    list = check_status_rpi(element.serial, element.os)
                    rpi_power_status.append(list)
            if flag is False:
                list = check_status_rpi(serial, "None")
                rpi_power_status.append(list)
                flag = False

        return PowerStatus(
            power_status=rpi_power_status
        )
    else:
        list_serials = []

        flag = False
        if unavailable != "[]":
            for rpi in unavailable:
                if user == rpi.user:
                    flag = True
                    list = ListSerials(
                        serial=rpi.serial,
                        os=rpi.os
                    )
                    list_serials.append(list)

            if flag is False:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"The user '{user}' does not have"
                        f" any Raspberry Pi set up in the system."
                    )
                )

        for element in list_serials:
            list = check_status_rpi(element.serial, element.os)
            rpi_power_status.append(list)

    return PowerStatus(
        power_status=rpi_power_status
    )
