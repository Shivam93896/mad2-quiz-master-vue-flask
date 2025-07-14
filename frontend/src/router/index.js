import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '@/components/HelloWorld.vue'
import Login from '@/components/login.vue'
import Admin from '@/components/Admin.vue'
import Signup from '@/components/Signup.vue'
import Manage_subject from '@/components/Manage_subject.vue'
import AddChapter from '@/components/AddChapter.vue'
import Manage_Quiz from '@/components/Manage_Quiz.vue'
import Add_Question from '@/components/Add_Question.vue'
import View_Question from '@/components/View_Question.vue'
import Usre from '@/components/User.vue'
import StartQuiz from '@/components/StartQuiz.vue'
import User_Result from '@/components/User_Result.vue'
import Admin_User from '@/components/Admin_User.vue'
import Admin_Summary from '@/components/Admin_Summary.vue' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: '/',
        name: 'Home',
        component: HelloWorld,
    },  
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/manage_subject',
      name: 'manage_subject',
      component: Manage_subject,
      
    },
    {
      path: '/add_chapter/:sub_id',
      name: 'add_chapter',
      component: AddChapter,
    },
    {
      path: '/manage_quiz/',
      name: 'manage_quiz',
      component: Manage_Quiz,
    },
    {
      path: '/add_question/:quiz_id',
      name: 'add_question',
      component: Add_Question,
    },
    {
      path: '/view_question/:quiz_id',
      name: 'view_question',
      component: View_Question,
    },
    {
      path: '/user',
      name: 'user',
      component: Usre,
    },
    {
      path: '/start_quiz/:quiz_id',
      name: 'start_quiz',
      component: StartQuiz,
    },
    {
      path: '/user_result',
      name: 'user_result',
      component: User_Result,
    },
    {
      path: '/admin_user',
      name: 'admin_user',
      component: Admin_User,  
    },
    {
      path: '/admin_summary',
      name: 'admin_summary',
      component: Admin_Summary,
    }
  ],
})

export default router;
