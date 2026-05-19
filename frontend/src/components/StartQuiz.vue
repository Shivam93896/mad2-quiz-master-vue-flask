<template>
  <div class="container py-5">
    <div class="card shadow-lg">
      <div class="card-header bg-primary text-white text-center">
        <h2 class="fw-bold mb-0">{{ Quiztitle }}</h2>
      </div>

      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="text-muted mb-0">Time Left:</h5>
          <span class="badge bg-warning text-dark fs-5">{{ formatTime }}</span>
        </div>

        <div v-if="!QuizSubmitted">
          <form @submit.prevent="submitQuiz">
            <div
              v-for="(question, index) in questions"
              :key="index"
              class="mb-5 border-bottom pb-3"
            >
              <h5 class="mb-3">
                {{ index + 1 }}. {{ question.question_state }}
              </h5>
              <div
                class="form-check"
                v-for="(option, optionIndex) in question.options"
                :key="optionIndex"
              >
                <input
                  class="form-check-input"
                  type="radio"
                  :name="'question-' + index"
                  v-model="userAnswers[question.id]"
                  :value="option"
                  :disabled="timeleft <= 0"
                />
                <label class="form-check-label">{{ option }}</label>
              </div>
            </div>
            <div class="text-center">
              <button type="submit" class="btn btn-success px-5 py-2">
                Submit Quiz
              </button>
            </div>
          </form>
        </div>

        <div v-else>
          <div class="alert alert-success text-center" role="alert">
            <h5 class="mb-0">Quiz submitted successfully!</h5>
          </div>

          <h4 class="text-primary mb-4">Quiz Results</h4>
          <div
            v-for="(question, index) in questions"
            :key="index"
            class="mb-4 border-bottom pb-3"
          >
            <h5>{{ index + 1 }}. {{ question.question_state }}</h5>
            <p
              :class="{
                'text-danger': userAnswers[question.id] !== correctAnswers[question.id],
                'text-success': userAnswers[question.id] === correctAnswers[question.id],
              }"
              class="fw-semibold"
            >
              Your answer: {{ userAnswers[question.id] || 'Not answered' }}
            </p>
            <p v-if="userAnswers[question.id] !== correctAnswers[question.id]" 
              class="text-success fw-semibold">
              Correct answer: {{ correctAnswers[question.id] }}
           </p>
            
          </div>
          <div class="text-center mt-4">
            <router-link to="/user" class="btn btn-outline-primary">
              Back to Quizzes
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>

export default {
    name: 'StartQuiz',
    data() {
        return {
            Quiztitle: '',
            userAnswers: {},
            correctAnswers: {},
            questions: [],
            QuizSubmitted: false,
            timeleft: 0, 
            timelimit: 0, 
            timer: null,

        };
    },
    computed: {
        formatTime() {
            const minutes = Math.floor(this.timeleft / 60);
            const seconds = this.timeleft % 60;
            return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        },
        filteredQuizzes() {
            const subject = this.$route.params.subject;
            return this.quizzes.filter(quiz => quiz.subject === subject);
        }
    },
    methods: {
        async fetchQuiz() {
            const response = await fetch(`https://mad2-quiz-master-vue-flask-7.onrender.com//start_quiz/${this.$route.params.quiz_id}`,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": 'Bearer '+ localStorage.getItem('user_token')
            },
        });
        const data = await response.json();
        this.Quiztitle = data.quiz_name;
        this.timelimit = data.time_limit; 
        this.timeleft = this.timelimit ; 
        this.questions = data.questions.map(question => {
            this.correctAnswers[question.id] = question.correct_answer;
            return {
                id:question.id,
                question_state: question.question_state,
                options: [question.option1, question.option2, question.option3, question.option4],  
            };
            });
        
        
        },
        startCountdown() {
           this.timer = setInterval(() => {
                this.timeleft--;
                if (this.timeleft <= 0) {
                    clearInterval(this.timer);
                    this.submitQuiz();
                }
            }, 1000);
        },
        prepareAnswer(){
            const lettermap = ['a','b','c','d'];
            const answers = {};
            this.questions.forEach(question => {
                answers[question.id] = lettermap[question.options.indexOf(this.userAnswers[question.id])];
            });
            return answers;
        },

        async submitQuiz() {
            clearInterval(this.timer);
            this.QuizSubmitted = true;
            const payload = {
                correct_option: this.prepareAnswer()
            };
            fetch(`https://mad2-quiz-master-vue-flask-7.onrender.com//start_quiz/${this.$route.params.quiz_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "authorization": 'Bearer ' + localStorage.getItem('user_token')
                },
                body: JSON.stringify(payload)   
            })
              .then((response) => response.json())
              .then((data) => {
                this.score = data.score;
                this.total_possible_score = data.total_possible_score;
                this.precent = data.precent;
                this.QuizSubmitted = true;
                alert(data.message);
              })
            
            
        
        
        }
    },
    mounted() {
        this.fetchQuiz();
        this.startCountdown();
    }


}

</script>