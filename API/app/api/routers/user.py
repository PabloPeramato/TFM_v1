from fastapi import APIRouter, Query
from app.models.schemas import (
    UserMetadata,
    OSMetadata
)
from app.utils.helpers import (
    check_folders,
    mount_array
)

router = APIRouter()


@router.get("/metadata", tags=["users"])
def users_metadata(
        user: str = Query(
            ...,
            description="Name of the user who has logged in"
        ),
        ) -> UserMetadata:

    command = f"ls /mnt/SESSIONS/{user}"
    output = check_folders(command).strip() + '\n'

    output_os = mount_array(output)

    operating_system = []
    for opsys in output_os:
        command += f"ls /mnt/SESSIONS/{user}/{opsys}"
        serial_output = check_folders(command).strip() + '\n'

        serial_numbers = mount_array(serial_output)
        serial_numbers = [s for s in serial_numbers if not s.endswith(':')]

        list = OSMetadata(
            name=opsys,
            serials=serial_numbers
        )

        operating_system.append(list)

    return UserMetadata(
        user=user,
        operating_systems=operating_system
    )
