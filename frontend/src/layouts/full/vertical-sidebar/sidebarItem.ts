import { DashboardIcon, DeviceDesktopIcon } from 'vue-tabler-icons';

export interface menu {
  header?: string;
  title?: string;
  icon?: object;
  to?: string;
  divider?: boolean;
  chip?: string;
  chipColor?: string;
  chipVariant?: string;
  chipIcon?: string;
  children?: menu[];
  disabled?: boolean;
  type?: string;
  subCaption?: string;
}

const sidebarItem: menu[] = [
  { divider: true },
  {
    title: 'Dashboard',
    icon: DashboardIcon,
    to: '/dashboard/default'
  },
  {
    title: 'My Devices',
    icon: DeviceDesktopIcon,
    to: '/my-devices'
  }
];

export default sidebarItem;
