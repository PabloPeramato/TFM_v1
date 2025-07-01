from fastapi import APIRouter, Query, HTTPException
from app.core.ssh_utils import run_command
from app.core.config import settings
from app.models.schemas import StatusOK
from app.utils.helpers import (
    check_folders,
    is_folder_empty,
    is_raspberry_pi_online
)
from app.api.routers.power import (
    power_on
)

router = APIRouter()


@router.post("/mount", tags=["sessions"])
def sessions_mount(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        os: str = Query(
            ...,
            description=(
                "Operating system name and Raspberry Pi model,"
                "found in GET /availability/software"
            )
        ),
        serial: str = Query(
            ...,
            description=(
                "Serial number of the Raspberry Pi to be used,"
                "found in GET /availability/hardware"
            )
        ),
        ) -> StatusOK:

    os = os.upper()
    serial = serial.lower()

    # Verificar si existen las carpetas en /PXE/boot y /PXE/filesystems
    command = (
        f"if ls /PXE/boot | grep -q '^{serial}$' ||"
        f"ls /PXE/filesystems | grep -q '^{serial}$';"
        f"then echo 'exists'; fi"
    )
    if check_folders(command):
        raise HTTPException(
            status_code=400,
            detail="You must unmount first before mounting a new session."
        )

    if os not in settings.OPERATING_SYSTEMS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid operating system, not registered,"
                " or incorrectly referenced."
            )
        )

    path_boot = f"/mnt/SESSIONS/{user}/{os}/{serial}/boot/{serial}"
    path_file = f"/mnt/SESSIONS/{user}/{os}/{serial}/filesystems/{serial}"
    command = (
        f"sudo cp -rp {path_boot} /PXE/boot && "
        f"sudo cp -rp {path_file} /PXE/filesystems"
    )

    run_command(
        command,
        settings.REMOTE_HOST_PXE,
        settings.USERNAME_PXE,
        settings.PASSWORD_PXE
    )

    return StatusOK(
        status=200,
        message=(
            f"User session \"{user}\" with the operating system \"{os}\""
            f" successfully mounted on the Raspberry Pi"
            f" with serial \"{serial}\"."
        )
    )


@router.post("/dismount", tags=["sessions"])
def sessions_dismount(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        os: str = Query(
            ...,
            description=(
                "Operating system name and Raspberry Pi model,"
                " found in GET /availability/software"
            )
        ),
        serial: str = Query(
            ...,
            description=(
                "Serial number of the Raspberry Pi to be used,"
                " found in GET /availability/hardware"
            )
        ),
        ) -> StatusOK:

    os = os.upper()
    serial = serial.lower()

    if os not in settings.OPERATING_SYSTEMS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid operating system, not registered,"
                " or incorrectly referenced."
            )
        )

    if serial == "85d959ed":
        remote_host_raspi = settings.REMOTE_HOST_RPI3_85D9
    elif serial == "81b715b7":
        remote_host_raspi = settings.REMOTE_HOST_RPI3_81B7
    elif serial == "8ba14c83":
        remote_host_raspi = settings.REMOTE_HOST_RPI3_8BA1
    elif serial == "1718561b":
        remote_host_raspi = settings.REMOTE_HOST_RPI4_1718

    if is_raspberry_pi_online(remote_host_raspi):
        raise HTTPException(
            status_code=400,
            detail=(
                f"The Raspberry Pi with the serial {serial}S"
                " must be powered off to unmount the image."
            )
        )

    command_users = (
        f"if ls /mnt/SESSIONS | grep -q '^{user}$';"
        f" then echo 'exists'; fi"
    )
    command_os = (
        f"if ls /mnt/SESSIONS/{user} | grep -q '^{os}$';"
        f" then echo 'exists'; fi"
    )
    command_directories = (
        f"if ls /mnt/SESSIONS/{user}/{os} | grep -q '^{serial}$';"
        f" then echo 'exists'; fi"
    )

    path_boot = f"/mnt/SESSIONS/{user}/{os}/{serial}/boot"
    path_file = f"/mnt/SESSIONS/{user}/{os}/{serial}/filesystems"
    if (check_folders(command_users).strip() != 'exists' or
            check_folders(command_os).strip() != 'exists' or
            check_folders(command_directories).strip() != 'exists'):

        command = (
            f"sudo mkdir -p {path_boot} && "
            f"sudo mkdir {path_file} && "
            f"sudo mv /PXE/boot/{serial} {path_boot} && "
            f"sudo mv /PXE/filesystems/{serial} {path_file}"
        )
    else:
        command = (
            f"sudo rm -rf {path_boot}/{serial} && "
            f"sudo rm -rf {path_file}/{serial} && "
            f"sudo mv /PXE/boot/{serial} {path_boot} && "
            f"sudo mv /PXE/filesystems/{serial} {path_file}"
        )

    run_command(
        command,
        settings.REMOTE_HOST_PXE,
        settings.USERNAME_PXE,
        settings.PASSWORD_PXE
    )

    return StatusOK(
        status=200,
        message=(
            f"User session \"{user}\" with the operating system \"{os}\""
            f" successfully dismounted on the Raspberry Pi"
            f" with serial \"{serial}\"."
        )
    )


@router.post("/newImage", tags=["sessions"])
def sessions_new_image(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        os: str = Query(
            ...,
            description=(
                "Operating system name and Raspberry Pi model,"
                " found in GET /availability/software"
            )
        ),
        serial: str = Query(
            ...,
            description=(
                "Serial number of the Raspberry Pi to be used,"
                " found in GET /availability/hardware")
        ),
        ) -> StatusOK:

    os = os.upper()
    serial = serial.lower()

    if os not in settings.OPERATING_SYSTEMS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid operating system, not registered,"
                " or incorrectly referenced."
            )
        )

    if os == "PI-3B-RASPBIAN-BULLSEYE" or os == "PI-3B-DIETPI-BOOKWORM":
        if serial not in settings.SERIAL_NUMBERS_3B:
            raise HTTPException(
                status_code=400,
                detail=(
                    "The serial does not correspond to any Raspberry Pi"
                    " compatible with the requested operating system."
                )
            )

    elif os == "PI-4B-RASPBIAN-BULLSEYE" or os == "PI-4B-DIETPI-BOOKWORM":
        if serial not in settings.SERIAL_NUMBERS_4B:
            raise HTTPException(
                status_code=400,
                detail=(
                    "The serial does not correspond to any Raspberry Pi"
                    " compatible with the requested operating system."
                )
            )

    # Verificar si existen las carpetas en /PXE/boot y /PXE/filesystems
    command = (
        f"if ls /PXE/boot | grep -q '^{serial}$' ||"
        f" ls /PXE/filesystems | grep -q '^{serial}$';"
        f" then echo 'exists'; fi"
    )

    if check_folders(command):
        raise HTTPException(
            status_code=400,
            detail="You must unmount first before creating a new image."
        )

    # /etc/sudoers
    sudoers_entry = f"{user} ALL=(ALL) ALL\n"

    # /etc/environment
    env_entry = f'OWNER_CHANGE="{user}"'

    command = ''
    path_sudoers = f"/PXE/filesystems/{serial}/etc/sudoers"
    path_environment = f"/PXE/filesystems/{serial}/etc/environment"
    if os == "PI-3B-RASPBIAN-BULLSEYE" or os == "PI-4B-RASPBIAN-BULLSEYE":
        path_cmdline = f"/mnt/IMAGES/{os}/CMDLINE_FILES/{serial}"
        path_images_boot = f"/mnt/IMAGES/{os}/boot/*"
        path_images_file = f"/mnt/IMAGES/{os}/filesystems/*"
        path_hostname = f"/mnt/IMAGES/{os}/HOSTNAME_FILES/{serial}/hostname"
        path_hosts = f"/mnt/IMAGES/{os}/HOSTS_FILES/{serial}/hosts"
        command = (
            f"sudo cp -rp {path_cmdline} /PXE/boot && "
            f"sudo cp -rp {path_images_boot} /PXE/boot/{serial} && "
            f"sudo mkdir /PXE/filesystems/{serial} && "
            f"sudo cp -rp {path_images_file} /PXE/filesystems/{serial} && "
            f"sudo cp -rp {path_hostname} /PXE/filesystems/{serial}/etc && "
            f"sudo cp -rp {path_hosts} /PXE/filesystems/{serial}/etc && "
            f"echo '{sudoers_entry}' | sudo tee -a {path_sudoers} && "
            f"echo '{env_entry}' | sudo tee -a {path_environment}"
        )

    elif os == "PI-3B-DIETPI-BOOKWORM" or os == "PI-4B-DIETPI-BOOKWORM":
        path_images_boot = f"/mnt/IMAGES/{os}/{serial}/boot/*"
        path_images_file = f"/mnt/IMAGES/{os}/{serial}/filesystems/*"
        command = (
            f"sudo mkdir /PXE/boot/{serial} && "
            f"sudo mkdir /PXE/filesystems/{serial} && "
            f"sudo cp -rp {path_images_boot} /PXE/boot/{serial} && "
            f"sudo cp -rp {path_images_file} /PXE/filesystems/{serial} && "
            f"echo '{sudoers_entry}' | sudo tee -a {path_sudoers} && "
            f"echo '{env_entry}' | sudo tee -a {path_environment}"
        )

    run_command(
        command,
        settings.REMOTE_HOST_PXE,
        settings.USERNAME_PXE,
        settings.PASSWORD_PXE
    )

    if os == "PI-3B-RASPBIAN-BULLSEYE" or os == "PI-4B-RASPBIAN-BULLSEYE":
        power_on(
            "user",
            serial
        )
    elif os == "PI-3B-DIETPI-BOOKWORM" or os == "PI-4B-DIETPI-BOOKWORM":
        power_on(
            "dietpi",
            serial
        )

    return StatusOK(
        status=200,
        message=(
            f"New image for user \"{user}\" with the operating system \"{os}\""
            f" successfully created for the Raspberry Pi"
            f" with serial \"{serial}\"."
        )
    )


@router.delete("/delete", tags=["sessions"])
def sessions_delete(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        os: str = Query(
            ...,
            description=(
                "Operating system name and Raspberry Pi model,"
                " found in GET /availability/software"
            )
        ),
        serial: str = Query(
            ...,
            description=(
                "Serial number of the Raspberry Pi to be used,"
                " found in GET /availability/hardware"
            )
        ),
        ) -> StatusOK:

    os = os.upper()
    serial = serial.lower()

    # Verificar si existen las carpetas en /PXE/boot y /PXE/filesystems
    command = (
        f"if ls /PXE/boot | grep -q '^{serial}$' ||"
        f" ls /PXE/filesystems | grep -q '^{serial}$';"
        f" then echo 'exists'; fi"
    )

    if check_folders(command):
        raise HTTPException(
            status_code=400,
            detail="You must unmount first before deleting a stored session.")

    if os not in settings.OPERATING_SYSTEMS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid operating system, not registered,"
                " or incorrectly referenced."
            )
        )

    command = ""
    command_os = (
        f"if ls /mnt/SESSIONS/{user} | grep -q '^{os}$';"
        f" then echo 'exists'; fi"
    )

    if check_folders(command_os).strip() == 'exists':
        command = (
            f"sudo rm -rf /mnt/SESSIONS/{user}/{os}/{serial}"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail=f"There is no folder for the operating system '{os}'."
        )

    run_command(
        command,
        settings.REMOTE_HOST_PXE,
        settings.USERNAME_PXE,
        settings.PASSWORD_PXE
    )

    array = settings.SERIAL_NUMBERS_3B + settings.SERIAL_NUMBERS_4B
    # Comprobar si la carpeta /mnt/SESSIONS/{usuario}/{os} está vacía
    path = f"/mnt/SESSIONS/{user}/{os}"
    if is_folder_empty({path}, array).strip() == 'false':
        # Si está vacía, eliminar la carpeta {os}
        command_delete_model = f"sudo rm -rf /mnt/SESSIONS/{user}/{os}"
        run_command(
            command_delete_model,
            settings.REMOTE_HOST_PXE,
            settings.USERNAME_PXE,
            settings.PASSWORD_PXE
        )

    return StatusOK(
        status=200,
        message=(
            f"User session \"{user}\" with the operating system \"{os}\""
            f" for the Raspberry Pi with serial \"{serial}\""
            f" successfully deleted."
        )
    )
