const MainRoutes = {
  path: '/main',
  meta: {
    requiresAuth: true
  },
  redirect: '/main/dashboard/default',
  component: () => import('@/layouts/full/FullLayout.vue'),
  children: [
    {
      name: 'LandingPage',
      path: '/',
      component: () => import('@/views/dashboards/default/DefaultDashboard.vue')
    },
    {
      name: 'Default',
      path: '/dashboard/default',
      component: () => import('@/views/dashboards/default/DefaultDashboard.vue')
    },
    {
      name: 'MyDevices',
      path: '/my-devices',
      component: () => import('@/views/myDevices/MyDevices.vue')
    },
    {
      name: 'DeviceDetails',
      path: '/devices/:serial',
      component: () => import('@/views/dashboards/DeviceDetailsView.vue'),
    },
    {
      name: 'MyDeviceDetails',
      path: '/my-devices/:serial',
      component: () => import('@/views/myDevices/MyDeviceDetailsView.vue'),
    }
  ]
};

export default MainRoutes;
