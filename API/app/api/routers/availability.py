from fastapi import APIRouter
from app.core.config import settings
from app.models.schemas import (
    HardwareAvailability,
    SoftwareAvailability,
    RpiStatus
)
from app.utils.helpers import (
    check_folders,
    mount_array
)

router = APIRouter()


@router.get("/hardware", tags=["availability"])
def availability_hardware() -> HardwareAvailability:
    command = "ls /PXE/filesystems"
    output = check_folders(command).strip() + '\n'

    output_serial_numbers = mount_array(output)
    rpi_unavailable_temp = []
    rpi_unavailable = []
    rpi_available = []
    serial_numbers = settings.SERIAL_NUMBERS_3B + settings.SERIAL_NUMBERS_4B

    for element in serial_numbers:
        if element in output_serial_numbers:
            rpi_unavailable_temp.append(element)
        else:
            rpi_available.append(element)

    for element in rpi_unavailable_temp:
        command = (
            f"if ls /PXE/boot/{element} | grep -q dietpi;"
            f" then echo 'exists'; fi"
        )

        if check_folders(command):
            osTemp = "dietpi"
        else:
            osTemp = "raspbian"

        command = (
            f"cut -d: -f1 /PXE/filesystems/{element}/etc/passwd"
        )

        output = check_folders(command).strip() + '\n'
        output_user = mount_array(output)
        list = RpiStatus(
            serial=element,
            os=osTemp,
            user=output_user.pop()
        )
        rpi_unavailable.append(list)

    return HardwareAvailability(
        available=rpi_available,
        unavailable=rpi_unavailable
    )


@router.get("/software", tags=["availability"])
def availability_software() -> SoftwareAvailability:
    command = "ls /mnt/IMAGES"
    output = check_folders(command).strip() + '\n'
    output_os = mount_array(output)

    return SoftwareAvailability(
        operating_systems=output_os
    )
