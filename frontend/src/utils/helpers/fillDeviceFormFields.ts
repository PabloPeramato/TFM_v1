import type { Ref } from 'vue';

type Device = {
    serial: string;
    os: string;
    user: string;
};

export function fillDeviceFormFields(
    device: Device | null,
    formUser: Ref<string>,
    formOs: Ref<string>,
    formSerial: Ref<string>,
    defaultUsername: string = ''
): void {
    if (!device) return;

    formUser.value = device.user !== '-' ? device.user : defaultUsername;
    formOs.value = device.os && device.os !== '-' ? device.os : '';
    formSerial.value = device.serial || '';
}
