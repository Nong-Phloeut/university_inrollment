<script setup>
const navItems = [
  {
    header: null,
    items: [
      { title: 'Dashboard', to: '/dashboard', icon: 'mdi-view-dashboard' },
    ],
  },
  {
    header: 'User Management',
    items: [
      { title: 'Instructors', to: '/users/instructors', icon: 'mdi-account' },
      { title: 'Students', to: '/users/student', icon: 'mdi-account-key' },
    ],
  },
  {
    header: 'Course Management',
    items: [
      { title: 'Course', to: '/course', icon: 'mdi-book' },
    ],
  },
  {
    header: 'Enrollment Management',
    items: [
      { title: 'Enrollment', to: '/enrollment', icon: 'mdi-book-arrow-right-outline' },
    ],
  },
  {
    header: 'Reports',
    items: [
      { title: 'Transcripts', to: '/reports/transcript', icon: 'mdi-transcribe' },
      // { title: 'Expired Items', to: '/reports/expired-items', icon: 'mdi-alert' },
    ],
  },
];
</script>

<template>
  <v-layout class="rounded rounded-md">
    <v-navigation-drawer>
      <v-list nav>
        <template v-for="(section, index) in navItems" :key="index">
          <v-list-subheader v-if="section.header">{{ section.header }}</v-list-subheader>

          <v-list-item
            v-for="(item, idx) in section.items"
            :key="idx"
            :title="item.title"
            :to="item.to"
            :prepend-icon="item.icon"
            link
          />
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar title="University Course Enrollment System"></v-app-bar>

    <v-main class="main">
      <v-container class="px-4 bg-background" fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-layout>
</template>
