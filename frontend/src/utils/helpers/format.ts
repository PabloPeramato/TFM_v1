export function formatDeviceName(serial: string) {
  return `Raspberry Pi - ${serial.slice(0, 4).toUpperCase()}`;
}
