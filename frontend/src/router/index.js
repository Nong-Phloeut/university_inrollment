import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "../views/DashboardView.vue";
import PharmacistsView from "../views/InstructorsView.vue";
import AdminsView from "../views/StudentView.vue";
import MedicationsView from "../views/CourseView.vue";
import DailySalesReport from "../views/Transcript.vue";
import ExpiredItemsReport from "../views/Enrollment.vue";
import LoginView from '../views/Login.vue'

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/",
    component: () => import("../views/Layout.vue"),
    children: [
      { path: "", redirect: "/dashboard" },
      { path: "dashboard", name: "Dashboard", component: DashboardView },
      {
        path: "users/instructors",
        name: "Pharmacists",
        component: PharmacistsView,
      },
      { path: "users/student", name: "Admins", component: AdminsView },
      {
        path: "course",
        name: "Medications",
        component: MedicationsView,
      },
      {
        path: "reports/transcript",
        name: "DailySales",
        component: DailySalesReport,
      },
      {
        path: "enrollment",
        name: "ExpiredItems",
        component: ExpiredItemsReport,
      },
    ],
  },
  {
    path: "/",
    redirect: "/dashboard",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   const isAuthenticated = !!localStorage.getItem('token') // or any auth check logic

//   if (to.path !== '/login' && !isAuthenticated) {
//     next('/login')
//   } else {
//     next()
//   }
// })

export default router;
