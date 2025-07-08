const MainRoutes = {
  path: '/main',
  meta: {
    requiresAuth: true
  },
  redirect: '/main/dashboard/default',
  component: () => import('@/layouts/full/FullLayout.vue'),
  children: [
    {
      name: 'Profile',
      path: '/profile',
      component: () => import('@/views/myProfile/views/myProfile.vue')
    },
    {
      name: 'LandingPage',
      path: '/',
      component: () => import('@/views/dashboards/views/DefaultDashboard.vue')
    },
    {
      name: 'Default',
      path: '/dashboard/default',
      component: () => import('@/views/dashboards/views/DefaultDashboard.vue')
    },
    {
      name: 'MyDevices',
      path: '/my-devices',
      component: () => import('@/views/myDevices/views/MyDevices.vue')
    },
    {
      name: 'DeviceDetails',
      path: '/devices/:serial',
      component: () => import('@/views/dashboards/views/DeviceDetailsView.vue'),
    },
    {
      name: 'MyDeviceDetails',
      path: '/my-devices/:serial',
      component: () => import('@/views/myDevices/views/MyDeviceDetailsView.vue'),
    }
  ]
};

export default MainRoutes;
