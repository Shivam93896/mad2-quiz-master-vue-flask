<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" >Admin Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="container mt-5">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="text-primary fw-bold">Questions for Quiz ID: {{ quizId }}</h1>
        <button class="btn btn-outline-secondary" @click="$router.go(-1)">⬅ Back</button>
      </div>

      <div v-if="questions.length === 0" class="alert alert-info text-center">
        No questions available for this quiz.
      </div>

      <div v-else class="card border-primary shadow-sm">
        <div class="card-body">
          <h5 class="card-title mb-3 text-primary">Questions List</h5>
          <div class="table-responsive">
            <table class="table table-bordered table-hover">
              <thead class="table-primary">
                <tr>
                  <th>Question</th>
                  <th>Question State</th>
                  <th>Options</th>
                  <th>Correct Answer</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="question in questions" :key="question.id">
                  <td>{{ question.question_tag }}</td>
                  <td>{{ question.question_state }}</td>
                  <td>
                    <ul class="mb-0">
                      <li>{{ question.option1 }}</li>
                      <li>{{ question.option2 }}</li>
                      <li>{{ question.option3 }}</li>
                      <li>{{ question.option4 }}</li>
                    </ul>
                  </td>
                  <td>{{ question.correct_option }}</td>
                  <td>
                    <button class="btn btn-warning btn-sm me-2" @click="updateQuestion(question)">Edit</button>
                    <button class="btn btn-danger btn-sm" @click="deleteQuestion(question.id)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Edit Question Modal -->
        <div class="modal fade" id="editQuestionModal" tabindex="-1" aria-labelledby="editQuestionModalLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h5 class="modal-title" id="editQuestionModalLabel">Edit Question</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                <!-- Form for editing question will go here -->
                <form @submit.prevent="submitEditedQuestion">
                    <div class="mb-3">
                        <label for="editQuestion" class="form-label">Question</label>
                        <input type="text" class="form-control" id="editQuestion" v-model="editedQuestion.question_tag" required>
                    </div>
                    <div class="mb-3">
                        <label for="editState" class="form-label">Question State</label>
                        <input type="text" class="form-control" id="editState" v-model="editedQuestion.question_state" required>
                    </div>
                    <div class="mb-3">
                        <label for="editOption1" class="form-label">Option A</label>
                        <input type="text" class="form-control" id="editOption1" v-model="editedQuestion.option1" required>
                    </div>
                    <div class="mb-3">
                        <label for="editOption2" class="form-label">Option B</label>
                        <input type="text" class="form-control" id="editOption2" v-model="editedQuestion.option2" required>
                    </div>
                    <div class="mb-3">
                        <label for="editOption3" class="form-label">Option C</label>
                        <input type="text" class="form-control" id="editOption3" v-model="editedQuestion.option3" required>
                    </div>
                    <div class="mb-3">
                        <label for="editOption4" class="form-label">Option D</label>
                        <input type="text" class="form-control" id="editOption4" v-model="editedQuestion.option4" required> 
                    </div>
                    <div class="mb-3">
                        <label for="editCorrectOption" class="form-label">Correct Answer</label>
                        <select class="form-select" id="editCorrectOption" v-model="editedQuestion.correct_option" required>
                            <option value="" disabled>Select correct answer</option>
                            <option value="option1">Option A</option>
                            <option value="option2">Option B</option>
                            <option value="option3">Option C</option>
                            <option value="option4">Option D</option>
                        </select>
                    </div>  
                    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                        <button type="submit" class="btn btn-success me-md-2">Update Question</button>
                        <button type="reset" class="btn btn-secondary" @click="resetForm">Reset</button>    
                    </div>
                </form>          
                </div>
            </div>
            </div>
        </div>   
    </div>
  </div>
</template>

<script>


export default {
  data() {
    return {
      questions: [],
      editedQuestion: {
            question_tag: '',
            question_state: '',
            option1: '',
            option2: '',
            option3: '',
            option4: '',
            correct_option: '',
        }

    };
  },
  computed: {
    quizId() {
      return this.$route.params.quiz_id;
    }
  },
  methods: {
    fetchQuestions() {
      fetch(`https://mad2-quiz-master-vue-flask-7.onrender.com//get_questions/${this.quizId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        }
      })
        .then(response => response.json())
        .then(data => {
          this.questions = data;
        })
        .catch(error => {
          console.error('Error fetching questions:', error);
        });
    },
    updateQuestion(question) {
        this.editedQuestion = question
        bootstrap.Modal.getOrCreateInstance(document.getElementById('editQuestionModal')).show();
    },
    submitEditedQuestion(){
        fetch(`https://mad2-quiz-master-vue-flask-7.onrender.com//edit_question/${this.editedQuestion.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
            'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
        body: JSON.stringify(this.editedQuestion)
        }) 
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            bootstrap.Modal.getInstance(document.getElementById('editQuestionModal')).hide();
            this.fetchQuestions();
        })   
 
    },
    deleteQuestion(questionId) {
      fetch(`https://mad2-quiz-master-vue-flask-7.onrender.com//delete_question/${questionId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ` + localStorage.getItem('admin_token')
        },
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);  
          this.fetchQuestions();
        });
        
    },
  },

  mounted() {
    this.fetchQuestions();
  }
};
</script>

<style scoped>
.table td,
.table th {
  vertical-align: middle;
}
.card {
  border-radius: 1rem;
}
</style>
